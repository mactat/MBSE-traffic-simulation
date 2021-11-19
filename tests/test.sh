#!/bin/bash
NUM_OF_FILES=$(ls | grep -c input)
FAILED=false
for i in $(seq 1 $NUM_OF_FILES);
do
    TEST_FAILED=false
    start=`date +%s.%N`
    python3 ../src/headless.py < "input$i.txt" 2>/dev/null > "output$i.txt" || TEST_FAILED=true && FAILED=true
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l )
    if [ "$TEST_FAILED" = true ]
    then
        echo -e "Test $i \e[031mfailed\e[0m.\nTime of the test: $runtime s\n"
    else
        RESULT=$( cat "output$i.txt" )
        echo -e "Test $i \e[32mdone\e[0m.\nOutput:\n$RESULT.\nTime of the test: $runtime s\n"
    fi
done 

if [ "$FAILED" = true ]
then
    exit 1
fi
