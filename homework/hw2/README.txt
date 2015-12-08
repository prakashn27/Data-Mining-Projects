Execution:
==========
hw2
Executing the apriori algorithm using the following command with default support(50) and confidence(70)

python apriori.py -f filename.txt

eg. python apriori.py -f association-rule-test-data.txt


For changing the support use the following command 
python apriori.py -f finename.txt -s 0.3
python apriori.py -f association-rule-test-data.txt -s 0.3


For changing the confidence use -c command
python apriori.py -f association-rule-test-data.txt -s 0.3 -c 0.7

for executing the templates use the following functions declared in the file.
Pass the corresponding variables for the templates

result, cnt = template1_helper("head", "none", ['gene1_up', 'gene10_down'], rule_with_val)

result, cnt = template2_helper("head", 2, rule_with_val)

result, cnt = template3("1or1", "RULE", "ANY", ['Gene1_UP'], "HEAD", 1, ['Gene59_UP'], rule_with_val)




