import os
import math
from astropy.io import fits
import warnings
from glob import glob
import photutils
from reproject import reproject_interp  # https://reproject.readthedocs.io/en/stable/
from tqdm import tqdm
from SExtractor import SExtractor
from stwcs.wcsutil import HSTWCS
from astropy.table import Table
from tweakwcs import fit_wcs, FITSWCS, TPMatch
from drizzlepac import updatehdr
import shutil


class PrepImg:
    
    ### INITIALIZE
    ### Only inputs are image directory, file naming pattern, and field name

    def __init__(self, image_dir, file, field, reproject=True, i2d=True):
        # Initialize image locations and future names
        self.image_dir = image_dir
        self.file = file
        self.field = field
        self.imfile = f'{self.field}_*_sci.fits'
        self.i2d = i2d
        self.reproject = reproject

        # Create empty data structures
        self.i2d_img = []
        self.sci_img = []
        self.wht_img = []
        self.bkg_img = []
        self.filts = []
        
        # Ignore astropy FITSFixedWarning
        warnings.simplefilter('ignore')

        ### GET I2D IMAGES
        ### Uses image_dir and file to find existing i2d images
        if type(self.file) == str: #single filename pattern
            self.i2d_img = glob(os.path.join(self.image_dir, self.file))
        
        else: # if file patterns specified as list/tuple
            for filename in self.file:
                for file in glob(os.path.join(self.image_dir, filename)):
                    self.i2d_img.append(file)

        self.i2d_img.sort()

        ### SPLIT I2D FILES
        ### Creates 'sci' and 'wht' files from the i2d images
        if self.i2d == True:
            for input_image in tqdm(self.i2d_img,desc='Saving individual images...'):
                lowercase_img = os.path.basename(input_image.lower())
                for i in range(len(lowercase_img)):
                    if lowercase_img[i] == 'f' and (lowercase_img[i+4] == 'w' or lowercase_img[i+4] == 'm') and lowercase_img[i+1] in '0 1 2 3 4 5 6 7 8 9'.split():
                        filt = lowercase_img[i:i+5].upper()
                        self.filts.append(filt)
                        break
                
                hdu_list = fits.open(input_image)
                header = hdu_list['sci'].header[:]
                
                # Only the science extension header has any info including WCS
                # So we'll just use that for all the output files

                for extension in 'sci wht'.split():
                    output_image = os.path.join(self.image_dir, f'{self.field}_{filt}_{extension}.fits')
                    
                    if extension == 'sci':
                        self.sci_img.append(output_image)
                    else:
                        self.wht_img.append(output_image)
                    
                    header['EXTNAME'] = extension
                    
                    fits.writeto(output_image, hdu_list[extension].data, header, overwrite=True)
                
                hdu_list.close()

        ### PUT SCI AND WHT IMAGES IN LISTS IF THESE ARE SUPPLIED INSTEAD OF I2D
        else:
            for input_image in tqdm(self.i2d_img,desc='Reading in individual images...'):
                new_image = input_image.replace('.fits', '_prep.fits')
                shutil.copy(input_image, new_image)
                input_image = new_image

                lowercase_img = os.path.basename(input_image.lower())
                for i in range(len(lowercase_img)):
                    if lowercase_img[i] == 'f' and (lowercase_img[i+4] == 'w' or lowercase_img[i+4] == 'm') and lowercase_img[i+1] in '0 1 2 3 4 5 6 7 8 9'.split():
                        filt = lowercase_img[i:i+5].upper()
                        break

                if 'sci' in input_image.lower() or 'drz' in input_image.lower():
                    self.sci_img.append(input_image)
                    self.filts.append(filt)

                elif 'wht' in input_image.lower():
                    self.wht_img.append(input_image)

            # remake file name pattern
            self.imfile = self.sci_img[0].replace(self.filts[0], '*')
                
        ### GET ZEROPOINTS
        ### Use pixel size in image header to calculate photometric zeropoints for SW and LW filters
        ### If SW and LW images have the same pixel size, zp_sw == zp_lw

        zeropoints = []
        for file in tqdm(self.sci_img, desc="Calculating zeropoints..."):
            hdul = fits.open(file)
            header = hdul[0].header
                        
            pixel_size = header['PIXAR_A2']**0.5
            zp = 8.9 - 2.5 * math.log10(1e+6 / ( (360 * 3600) / (2 * math.pi * pixel_size) )**2)
            zeropoints.append(zp)
                
            hdul.close()
            
        self.zp_sw = max(zeropoints)
        self.zp_lw = min(zeropoints)
                
        ### REPROJECT SCI AND WHT FILES
        ### Having the images on the same pixel grid will be beneficial for SExtractor

        if self.reproject == True:
            images = self.sci_img + self.wht_img
            for image in tqdm(images, desc='Reprojecting pixel grids...'):
                ref_image = self.sci_img[0]

                hdul = fits.open(ref_image)
                ref_header = hdul['sci'].header

                hdu = fits.open(image)
                data = hdu[0]

                reprojected_data, footprint = reproject_interp(data, ref_header)
                
                fits.writeto(image, reprojected_data.astype('float32'), ref_header, overwrite=True)
                hdu.close()
                hdul.close()

        ### DONE SPLITTING AND REPROJECTING
        ### Print
        
        print(f'Field: {self.field}\nImage Directory: {self.image_dir}\nImage File Pattern: {self.imfile}\n' +
              f'SW ZP: {self.zp_sw:.3f}\nLW ZP: {self.zp_lw:.3f}')
        
    ### Method bkgsub
    ### optionally subtract the background from the science images
    ### size is the size of each square that background is measured and subtracted from

    def bkgsub(self, size=100):
        for image in tqdm(self.sci_img, desc='Background Subtraction...'):
            hdul = fits.open(image)
            data = hdul['sci'].data

            background_map = photutils.Background2D(data, size, filter_size=5)  
            data = data - background_map.background.astype('float32')

            hdul['sci'].data = data
            newfile = image.replace(".fits", "_bkgsub.fits")
            self.bkg_img.append(newfile)
            hdul.writeto(newfile, overwrite=True)
            hdul.close()
            
        print(f'Field: {self.field}\nImage Directory: {self.image_dir}\nImage File Pattern: ' +
              f'{self.imfile.replace(".fits", "_bkgsub.fits")}')

    ### METHOD TWEAKWCS
    ### uses SExtractor to make catalogs for the images and aligns them based on that

    def tweakwcs(self, cat_dir, config_file, ref_filt = None, overwrite=False):

        # set reference filter if not specified
        if ref_filt == None:
            ref_idx = 0
            ref_filt = self.filts[ref_idx]
        
        # get index of reference filter if specified
        else:
            ref_filt = ref_filt.upper()
            ref_idx = self.filts.index(ref_filt)

        # initialize sextractor object
        s = SExtractor(self.field, self.image_dir, self.imfile, cat_dir, (self.zp_sw, self.zp_lw))
        
        # make sextractor catalogs
        print('Running SourceExtractor...')
        s.sextract(config_file, overwrite=overwrite, verbose=False)

        # retrieve sextractor catalogs
        cats = glob(os.path.join(cat_dir, f'{self.field}_*_cat.txt'))
        
        # create list of catalogs corresponding to each filter
        self.cats = []
        for filt in self.filts:
            for file in cats:
                if filt.upper() in file:
                    self.cats.append(file)

        # set up reference filter images
        ref_image = self.sci_img[ref_idx]
        ref_hdul = fits.open(ref_image)
        ref_header = ref_hdul[0].header
#        ref_wcs = HSTWCS(ref_hdul, 0)

        # reference filter catalog
        ref_catfile = self.cats[ref_idx]
        ref_cat = Table.read(ref_catfile, format='ascii')
        ref_cat.rename_column('X_IMAGE', 'x')
        ref_cat.rename_column('Y_IMAGE', 'y')
        ref_cat.rename_column('ALPHA_J2000', 'RA')
        ref_cat.rename_column('DELTA_J2000', 'DEC')

        for idx in tqdm(range(len(self.filts)), desc='Tweaking images...'):
            filt = self.filts[idx]

            # make sure input filter isn't same as reference filter:
            if idx == ref_idx:
                continue

            # input filter images
            input_image = self.sci_img[idx]
            wht_image = self.wht_img[idx]
            input_hdul = fits.open(input_image)
            input_wht_hdul = fits.open(wht_image)
#            input_header = input_hdul[0].header
            input_wcs = HSTWCS(input_hdul, 0)

            # input filter catalog
            input_catfile = self.cats[idx]
            input_cat = Table.read(input_catfile, format='ascii')
            input_cat.rename_column('X_IMAGE', 'x')
            input_cat.rename_column('Y_IMAGE', 'y')
            input_cat.rename_column('ALPHA_J2000', 'RA')
            input_cat.rename_column('DELTA_J2000', 'DEC')

            # match catalogs with loop
            xi_best = 0
            yi_best = 0
            matches_best = 0

            for xi in range(-3, 3):
                for yi in range(-3, 3):
                    match = TPMatch(searchrad=10, separation=1, tolerance=2, use2dhist=True, xoffset=xi, yoffset=yi)
                    input_wcs_corrector = FITSWCS(input_wcs)
                    ridx, iidx = match(ref_cat, input_cat, input_wcs_corrector)

                    if len(ridx) >= matches_best:
                        xi_best = xi
                        yi_best = yi
                        matches_best = len(ridx)
            
            # match catalogs based on best offset
            match = TPMatch(searchrad=10, separation=1, tolerance=2, use2dhist=True, xoffset=xi_best, yoffset=yi_best)
            input_wcs_corrector = FITSWCS(input_wcs)
            ridx, iidx = match(ref_cat, input_cat, input_wcs_corrector)

            # make sure number of matches isn't bad
            if len(ridx) < 50:
                print('Matching failed: fewer than 50 matches found.')

            # else continue with the matching
            else:
                # tweak wcs of input image
                aligned_imwcs = fit_wcs(ref_cat[ridx], input_cat[iidx], input_wcs_corrector).wcs
                updatehdr.update_wcs(input_hdul, 0, aligned_imwcs, wcsname='TWEAK', reusename=True, verbose=False)
                updatehdr.update_wcs(input_wht_hdul, 0, aligned_imwcs, wcsname='TWEAK', reusename=True, verbose=False)
                
                # reproject sci
                reprojected_data, footprint = reproject_interp(input_hdul[0], ref_header)
                fits.writeto(input_image, reprojected_data.astype('float32'), ref_header, overwrite=True)
                # reproject wht
                reprojected_data, footprint = reproject_interp(input_wht_hdul[0], ref_header)
                fits.writeto(wht_image, reprojected_data.astype('float32'), ref_header, overwrite=True)

            input_hdul.close()
        
        ref_hdul.close()
