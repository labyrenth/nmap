#!/usr/bin/env bash
set -e
set -u

function usage {
	echo "Usage:"
	echo "$0 {path to extracted file system of firmware}\
 {optional: name of the file to store results - defaults to firmwalker.txt}"
	echo "Example: ./$0 linksys/fmk/rootfs/"
	exit 1
}

function getArray {
    array=() # Create array
    while IFS= read -r line
    do
        array+=("$line")
    done < "$1"
}

# Check for arguments
if [[ $# -gt 1 || $# -lt 1 ]]; then
    usage
fi

# Set variables
FIRMDIR=$1
origin_dir=`dirname $0`
# make result directory when if directory does not exit
RESULT="$origin_dir/result"
if [ ! -d $RESULT ]; then
	mkdir $RESULT
fi

# Remove previous file if it exists, is a file and doesn't point somewhere
DATE=$(date +"%Y%m%d_%H%M")
FOLDER=$RESULT/$DATE
if [ -d $FOLDER ]; then
    rm -rf $FOLDER
fi
mkdir $FOLDER

# Perform searches
getArray "$origin_dir/data/passfiles"
passfiles=("${array[@]}")
for passfile  in "${passfiles[@]}"
do
    find $FIRMDIR -name $passfile | cut -c${#FIRMDIR}- | tee -a $FOLDER/passfiles 1> /dev/null
done

#FIND Unix-MD5-HASHES
egrep -sro '\$1\$\w{8}\S{23}' $FIRMDIR | tee -a $FOLDER/md5_hashes

#/etc/ssl file Check
if [[ -d "$FIRMDIR/etc/ssl" ]]; then
    ls -l $FIRMDIR/etc/ssl >> $FOLDER/etc_sslfiles
fi

#FIND sslfiles
getArray "$origin_dir/data/sslfiles"
sslfiles=("${array[@]}")
for sslfile in ${sslfiles[@]}
do
    find $FIRMDIR -name $sslfile | cut -c${#FIRMDIR}- | tee -a $FOLDER/data_sslfiles
       certfiles=( $(find ${FIRMDIR} -name ${sslfile}) )
       : "${certfiles:=empty}"
       # Perform Shodan search. This assumes Shodan CLI installed with an API key.
       if [ "${certfiles##*.}" = "pem" ] || [ "${certfiles##*.}" = "crt" ]; then
          for certfile in "${certfiles[@]}"
          do
             serialno=$(openssl x509 -in $certfile -serial -noout) || echo "Incorrect File Content:Continuing"
             serialnoformat=(ssl.cert.serial:${serialno##*=})
             if type "shodan" &> /dev/null ; then
                 shocount=$(shodan count $serialnoformat)
                 if (( $shocount > 0 )); then
            		echo $certfile | cut -c${#FIRMDIR}- >> $FOLDER/shodan
            		echo $serialno >> $FOLDER/shodan
                         	echo "Number of devices found in Shodan =" $shocount >> $FOLDER/shodan
            		cat $certfile >> $FOLDER/shodan
                 fi
             else 
                echo "Shodan cli not found."
             fi
          done
       fi
done

getArray "$origin_dir/data/sshfiles"
sshfiles=("${array[@]}")
for sshfile in ${sshfiles[@]}
do
    find $FIRMDIR -name $sshfile | cut -c${#FIRMDIR}- >> $FOLDER/sshfiles
done
getArray "$origin_dir/data/files"
files=("${array[@]}")
for file in ${files[@]}
do
    find $FIRMDIR -name $file | cut -c${#FIRMDIR}- >> $FOLDER/config_files
done
getArray "$origin_dir/data/dbfiles"
dbfiles=("${array[@]}")
for dbfile in ${dbfiles[@]}
do
    find $FIRMDIR -name $dbfile | cut -c${#FIRMDIR}- >> $FOLDER/dbfiles
done
find $FIRMDIR -name "*.sh" | cut -c${#FIRMDIR}- >> $FOLDER/sh_files
find $FIRMDIR -name "*.bin" | cut -c${#FIRMDIR}- >> $FOLDER/bin_files
getArray "$origin_dir/data/patterns"
patterns=("${array[@]}")
PATTERN_FOLDER="$FOLDER/patterns"
if [ ! -d $PATTERN_FOLDER ]; then
    mkdir $PATTERN_FOLDER
fi
for pattern in "${patterns[@]}"
do
    grep -lsirnw $FIRMDIR -e "$pattern" | cut -c${#FIRMDIR}- | tee -a $PATTERN_FOLDER/$pattern 1> /dev/null
done
getArray "$origin_dir/data/webservers"
webservers=("${array[@]}")
for webserver in ${webservers[@]}
do
    find $FIRMDIR -name "$webserver" | cut -c${#FIRMDIR}- >> $FOLDER/webservers
done
getArray "$origin_dir/data/binaries"
binaries=("${array[@]}")
for binary in "${binaries[@]}"
do
    find $FIRMDIR -name "$binary" | cut -c${#FIRMDIR}- >> $FOLDER/binaries
done

grep -sRIEho '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' --exclude='console' $FIRMDIR | sort | uniq >> $FOLDER/IP

grep -sRIEoh '(http|https)://[^/"]+' --exclude='console' $FIRMDIR | sort | uniq >> $FOLDER/url

grep -sRIEoh '([[:alnum:]_.-]+@[[:alnum:]_.-]+?\.[[:alpha:].]{2,6})' "$@" --exclude='console' $FIRMDIR | sort | uniq >> $FOLDER/emails

#Perform static code analysis 
#eslint -c eslintrc.json $FIRMDIR | tee -a $FILE

