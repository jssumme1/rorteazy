#!/bin/bash
#
# Requires bash version >= 4
# 
# The script uses the command line tool 'curl' for querying
# the MAST Download service for public and protected data. 
#

type -P curl >&/dev/null || { echo "This script requires curl. Exiting." >&2; exit 1; }



# Check for existing Download Folder
# prompt user for overwrite, if found
let EXTENSION=0
FOLDER=MAST_2022-12-05T1423
DOWNLOAD_FOLDER=$FOLDER
if [ -d $DOWNLOAD_FOLDER ]
then
  echo -n "Download folder ${DOWNLOAD_FOLDER} found, (C)ontinue writing to existing folder or use (N)ew folder? [N]> "
  read -n1 ans
  if [ "$ans" = "c" -o "$ans" = "C" ]
  then
    echo ""
    echo "Downloading to existing folder: ${DOWNLOAD_FOLDER}"
    CONT="-C -"
  else
    while [ -d $DOWNLOAD_FOLDER ]
    do
      ((EXTENSION++))
      DOWNLOAD_FOLDER="${FOLDER}-${EXTENSION}"
    done

    echo ""
    echo "Downloading to new folder: ${DOWNLOAD_FOLDER}"
  fi
fi

# mkdir if it doesn't exist and download files there. 
mkdir -p ${DOWNLOAD_FOLDER}

cat >${DOWNLOAD_FOLDER}/MANIFEST.HTML<<EOT
<!DOCTYPE html>
<html>
    <head>
        <title>MAST_2022-12-05T1423</title>
    </head>
    <body>
        <h2>Manifest for File: MAST_2022-12-05T1423</h2>
        <h3>Total Files: 7</h3>
        <table cellspacing="0" cellpadding="4" rules="all" style="border-width:5px; border-style:solid; border-collapse:collapse;">
            <tr>
                <td><b>URI</b></td>
                <td><b>File</b></td>
                <td><b>Access</b></td>
                <td><b>Status</b></td>
                <td><b>Logged In User</b></td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f356w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f356w/jw01345-o001_t021_nircam_clear-f356w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f200w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f200w/jw01345-o001_t021_nircam_clear-f200w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f150w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f150w/jw01345-o001_t021_nircam_clear-f150w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f277w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f277w/jw01345-o001_t021_nircam_clear-f277w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f444w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f444w/jw01345-o001_t021_nircam_clear-f444w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f115w_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f115w/jw01345-o001_t021_nircam_clear-f115w_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
            <tr>
                <td>mast:JWST/product/jw01345-o001_t021_nircam_clear-f410m_i2d.fits</td>
                <td>JWST/jw01345-o001_t021_nircam_clear-f410m/jw01345-o001_t021_nircam_clear-f410m_i2d.fits</td>
                <td>PUBLIC</td>
                <td>OK</td>
                <td>anonymous</td>
            </tr>
            
        </table>
    </body>
</html>

EOT

# Download Product Files:



cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f356w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f356w/jw01345-o001_t021_nircam_clear-f356w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f356w/jw01345-o001_t021_nircam_clear-f356w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f356w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f200w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f200w/jw01345-o001_t021_nircam_clear-f200w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f200w/jw01345-o001_t021_nircam_clear-f200w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f200w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f150w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f150w/jw01345-o001_t021_nircam_clear-f150w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f150w/jw01345-o001_t021_nircam_clear-f150w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f150w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f277w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f277w/jw01345-o001_t021_nircam_clear-f277w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f277w/jw01345-o001_t021_nircam_clear-f277w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f277w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f444w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f444w/jw01345-o001_t021_nircam_clear-f444w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f444w/jw01345-o001_t021_nircam_clear-f444w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f444w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f115w_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f115w/jw01345-o001_t021_nircam_clear-f115w_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f115w/jw01345-o001_t021_nircam_clear-f115w_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f115w_i2d.fits'





cat <<EOT
<<< Downloading File: mast:JWST/product/jw01345-o001_t021_nircam_clear-f410m_i2d.fits
                  To: ${DOWNLOAD_FOLDER}/JWST/jw01345-o001_t021_nircam_clear-f410m/jw01345-o001_t021_nircam_clear-f410m_i2d.fits
EOT

curl --globoff --location-trusted -f --progress-bar --create-dirs $CONT --output ./${DOWNLOAD_FOLDER}'/JWST/jw01345-o001_t021_nircam_clear-f410m/jw01345-o001_t021_nircam_clear-f410m_i2d.fits' 'https://mast.stsci.edu/api/v0.1/Download/file?bundle_name=MAST_2022-12-05T1423.sh&uri=mast:JWST/product/jw01345-o001_t021_nircam_clear-f410m_i2d.fits'




exit 0
