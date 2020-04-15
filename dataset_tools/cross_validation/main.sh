
#!/bin/bash


usage()
{
    echo "Usage: sysinfo_page. Parsing dataset into folds and trainin [[-f number of folders] [-d name of input dataset]]"
    exit
}

echo "a"

DST_NAME=""
FOLDS_NUM=""
SRC_DATATSET=""
# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -h | --help )           
            usage
            ;;
        -f | --folder )
            shift
            FOLDS_NUM=$1
            ;;
        -d | --dataset )
            shift
            SRC_DATATSET="$1"
            ;;
        * )                     
            usage
    esac
    shift
done

echo "a"

if [ "${SRC_DATATSET}" == "" ]; then
    usage
    echo "a"
fi


echo "Creating folds"
#python create_folds.py --src_dataset="${LOCAL_GIT}/dataset/exported/${SRC_DATATSET}" --number_of_folds="${FOLDS_NUM}" --dst_name="${SRC_DATATSET}"


for ((i=0;i<"${FOLDS_NUM}";i++)); 
do 
   # your-unix-command-here
   ./train.sh -d "folds/${SRC_DATATSET}/fold_${i}/train" -s "450" -i "$i"
done


