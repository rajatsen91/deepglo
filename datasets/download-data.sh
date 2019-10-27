#!/bin/bash
function gdrive-get() {
    fileid=$1
    filename=$2
    if [[ "${fileid}" == "" || "${filename}" == "" ]]; then
        echo "gdrive-curl gdrive-url|gdrive-fileid filename"
        return 1
    else
        if [[ ${fileid} = http* ]]; then
            fileid=$(echo ${fileid} | sed "s/http.*drive.google.com.*id=\([^&]*\).*/\1/")
        fi
        echo "Download ${filename} from google drive with id ${fileid}..."
        cookie="/tmp/cookies.txt"
        curl -c ${cookie} -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
        confirmid=$(awk '/download/ {print $NF}' ${cookie})
        curl -Lb ${cookie} "https://drive.google.com/uc?export=download&confirm=${confirmid}&id=${fileid}" -o ${filename}
        rm -rf ${cookie}
        return 0
    fi
}

gdrive-get 1UUwvY8Ixbwt3_fyDlJM80spZpgoOexRl electricity.npy
gdrive-get 1dyeYj8IJwZ3bKvk1H67eaDTANdapKe7w traffic.npy
gdrive-get 1VytXoL_vkrLqXxCR5IOXgE45hN2UL5oB wiki.npy
gdrive-get 1AE_s47dpRuSFgRREb_8jcVJij0kxaaHs pems.npy

#python reshape_data.py 
