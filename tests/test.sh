#!/bin/bash
NUM_OF_FILES=$(ls | grep -c input)
for i in $(seq 1 $NUM_OF_FILES);
do
    start=`date +%s.%N`
    python3 ../src/headless.py < "input$i.txt" > "output$i.txt"
    end=`date +%s.%N`

    RESULT=$( cat "output$i.txt" )
    runtime=$( echo "$end - $start" | bc -l )
    echo -e "Test $i \e[32mdone\e[0m.\nOutput: $RESULT.\nTime of the test: $runtime s\n"
done

