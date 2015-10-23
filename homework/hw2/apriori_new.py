import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
testing = False
result = True

def getItemSet(itemSet, transactionList, min_support, count):
    s = set()
    temp = defaultdict(int)
    if testing:
        print "getItemSet"
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                count[item] += 1
                temp[item] += 1

    for item, count in temp.items():
            support = float(count)/100
            # since number of transaction is 100 support = count /100
            if support >= min_support:
                    s.add(item)
    return s

def initData(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList


def calculateApriori(gen, min_support, min_conf):
    def calculateSupport(item):
        return float(count[item])/len(transactionList)
    itemSet, transactionList = initData(gen)
    if testing:
        print "len of item set is {0} and transaction is {1}".format(len(itemSet), len(transactionList))

    count = defaultdict(int)
    allItems = dict()
    assocRules = dict()
    # Dictionary which stores Association Rules

    initSet = getItemSet(itemSet, transactionList, min_support, count)
    tempSet = initSet
    # to count the total freqitemsets
    numberOfFreqItemSets = len(initSet)
    if result:
        print "Support >= {0} %".format(min_support * 100)
        print "Size of frequent itemset = {0} : {1}".format(1, len(initSet))
    k = 2
    while(tempSet != set([])):
        allItems[k-1] = tempSet
        # remove items which are less than min support
        tempSet = set([i.union(j) for i in tempSet for j in tempSet if len(i.union(j)) == k])
        cur = getItemSet(tempSet, transactionList, min_support, count)
        tempSet = cur
        numberOfFreqItemSets += len(tempSet)
        if result:
            print "Size of frequent itemset = {0} : {1}".format(k, len(tempSet))
        k = k + 1
    if result:
        print "Total = {0}".format(numberOfFreqItemSets)
  
    if testing:
        print "value of k is {0}".format(k)
        print "length of allItems is {0}".format(len(allItems))
        print "number of freq itemSet is {0}".format(len(allItems[k - 2]))
        # item set from previous iteration is in k-1 dictionary item

    if testing:
        print 'printing the count'
        print count
    def subsets(arr):
        if testing:
                print "subsets for " + str(arr)
        return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

    l = []
    for key, value in allItems.items()[1:]:
        for item in value:
            tempset = map(frozenset, [x for x in subsets(item)])
            for element in tempset:
                support = calculateSupport(item)
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = calculateSupport(item)/calculateSupport(element)
                    if confidence >= min_conf:
                        l.append(((list(element), list(remain)), (support, confidence)))
    return l

def printRules(rule_with_val):
    for rule, val in rule_with_val:
            body, head = rule
            support, confidence = val
            print "Rule: %s ==> %s , support = %.3f, confidence = %0.3f" % (str(body), str(head), support, confidence)
    print "Count of rules generated is {0}".format(len(rule_with_val))

# generate a rule string
def generateAndPrintRule(rule, val):
    body, head = rule
    support, confidence = val
    print "Rule: %s ==> %s , support = %.3f, confidence = %0.3f" % (str(body), str(head), support, confidence)

###########################################################################
# template generation
def template1(noun, val, geneList, rule_with_val):
    # template1("RULE", "ANY", ['G1_UP'])
    noun = noun.lower()
    geneList = map(lambda l: l.lower(), geneList)
    valArr = []
    inpSet = set()
    if not isinstance(val, int):
        # check for not integer
        val = val.lower()
    else:
        # it is an integer
        # generate combinations of list with val items for checking
        valSet = map(set,combinations(geneList, val))
        inpSet = set(geneList)
    print "printing the values"
    print noun, val, geneList
    for rule, value in rule_with_val:
        body, head = rule
        if noun == 'body':
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in body:
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    if not set(geneList).issubset(set(body)):
                        generateAndPrintRule(rule, value)
            else:
                for v in valSet:
                    if v.issubset(set(body)):
                        generateAndPrintRule(rule, value)
                        continue
        elif noun == 'head':
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in head:
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    if not set(geneList).issubset(set(head)):
                        generateAndPrintRule(rule, value)
            else:
                for v in valSet:
                    if v.issubset(set(head)):
                        generateAndPrintRule(rule, value)
                        continue
        elif noun == 'rule':
            ruleList = body + head
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in ruleList:
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    # for gene in geneList:
                    #     if not set(gene).issubset(set(ruleList)):
                    #         generateAndPrintRule(rule, value)
                    #         break
                    if not set(geneList).issubset(set(ruleList)):
                        generateAndPrintRule(rule, value)

            else:
                for v in valSet:
                    if v.issubset(set(ruleList)):
                        generateAndPrintRule(rule, value)
                        continue
    

def template2(noun, number, rule_with_val):
    #def template2("BODY", 2, ['G1_UP'])
    noun = noun.lower()
    for rule, val in rule_with_val:
        body, head = rule
        support, confidence = val
        if noun == 'body':
            if len(body) >= number:
                generateAndPrintRule(rule, val)
        elif noun == 'head':
            if len(head) >= number:
                generateAndPrintRule(rule, val)
        elif noun == 'rule':
            if len(body) + len(head) >= number:
                generateAndPrintRule(rule, val)
        else:
            print "not a valid template"
            break

def template1_helper(noun, val, geneList, rule_with_val):
    # template1("RULE", "ANY", ['G1_UP'])
    print "Generating Rules for the template given "
    print "========================================"
    resultList = []
    noun = noun.lower()
    geneList = map(lambda l: l.lower(), geneList)
    valArr = []
    inpSet = set()
    if not isinstance(val, int):
        # check for not integer
        val = val.lower()
    else:
        # it is an integer
        # generate combinations of list with val items for checking
        valSet = map(set,combinations(geneList, val))
        inpSet = set(geneList)
    # print "printing the values"
    # print noun, val, geneList
    totalRules = []
    for rule, value in rule_with_val:
        body, head = rule
        if noun == 'body':
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in body:
                            resultList.append(rule)
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    failed = False
                    for gene in geneList:
                        if gene in body:
                            failed = True
                            break
                    if not failed:
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)

            else:
                for v in valSet:
                    if v.issubset(set(body)) and not set(geneList) == set(body):
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)
                        continue
        elif noun == 'head':
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in head:
                            resultList.append(rule)
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    failed = False
                    for gene in geneList:
                        if gene in head:
                            failed = True
                            break
                    if not failed:
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)
                    # if not set(geneList).issubset(set(head)):
                    #     resultList.append(rule)
            else:
                for v in valSet:
                    if v.issubset(set(head)):
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)
                        continue
        elif noun == 'rule':
            ruleList = body + head
            if not isinstance(val, int):
                if val == 'any':
                    for gene in geneList:
                        if gene in ruleList:
                            resultList.append(rule)
                            generateAndPrintRule(rule, value)
                            continue
                elif val == 'none':
                    failed = False
                    for gene in geneList:
                        if gene in ruleList:
                            failed = True
                            break
                    if not failed:
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)
                    # if not set(geneList).issubset(set(ruleList)):
                    #     resultList.append(rule)

            else:
                for v in valSet:
                    if v.issubset(set(ruleList)) and not set(ruleList) == set(geneList):
                        resultList.append(rule)
                        generateAndPrintRule(rule, value)
                        continue
    # resultList = set(resultList)
    # resultList = [list(x) for x in set(tuple(x) for x in resultList)]
    print "No of rules generated for this templat is {0}".format(len(resultList))
    return resultList, len(resultList)

def template2_helper(noun, number, rule_with_val):
    print "Generating Rules for the template given "
    print "========================================"
    #def template2("BODY", 2, ['G1_UP'])
    resultList = []
    noun = noun.lower()
    for rule, val in rule_with_val:
        body, head = rule
        support, confidence = val
        if noun == 'body':
            if len(body) >= number:
                resultList.append(rule)
                generateAndPrintRule(rule, val)
        elif noun == 'head':
            if len(head) >= number:
                resultList.append(rule)
                generateAndPrintRule(rule, val)
        elif noun == 'rule':
            if len(body) + len(head) >= number:
                resultList.append(rule)
                generateAndPrintRule(rule, val)
        else:
            print "not a valid template"
            break
    print "Count of rules generated for this template is {0}".format(len(resultList))
    return resultList, len(resultList)

def template3(t, noun1, verb1, geneList1, noun2, verb2, l2, rule_with_val):
    # def template3("1or1", "BODY", "ANY", ['G1_UP'], "HEAD", 1, ['G59_UP'])
    if t == '1or1':
        #get 1 or 1
        # def template1_helper(noun, val, geneList, rule_with_val):
        result1, cnt = template1_helper(noun1, verb1, geneList1, rule_with_val)
        
        
        result1_whole = set()
        for item2 in result1:
            # print item
            (h, b) = item2
            result1_whole.add(frozenset(h + b))

        result2 , cnt = template2_helper(noun2, verb2, rule_with_val)
        # print result2[0]
        result2_whole = set()
        for item in result2:
            # print item
            (h, b) = item
            result2_whole.add(frozenset(h + b))
        print "length of first list {0}".format(len(result1_whole))

        print "length of second list {0}".format(len(result2_whole))
        # print result1_whole
        print result1_whole
        print result2_whole
        print len(result1_whole.union(result2_whole))
        # print len(result1_whole.intersection(result2_whole))


        # set(result1).union(set(result2))



# generate rule from template
def ruleForTemplate(rule_with_val, ruleTemplate, templateNo):
    # eg command line 
    # python apriori_new.py -f association-rule-test-data.txt -s 0.5 -c 0.7 -t 1 -r body-has-any-of-gene1_up

    # result which hold the data to be printed in string
    result = []
    if templateNo == 1:
        # {RULE|BODY|HEAD} HAS ({ANY|NUMBER|NONE}) OF (ITEMNO)
        # python apriori_new.py -f association-rule-test-data.txt -s 0.5 -c 0.7 -t 1 -r body-has-any-of-gene1_up
        ruleSplits = ruleTemplate.lower().split('-')
        noun, _ , verb, _ , item = ruleSplits 
        print noun, verb, item
        if not noun in ['body', 'head', 'rule']:
            print noun + " not associated with the rule"
            return
        if noun == 'body':
            # get the body part and check it
            for rule, val in rule_with_val:
                body, head = rule
                support, confidence = val
            print 'in if loop of body'
        elif noun == 'head':
            print 'head'
        elif noun == 'rule':
            print "entire rule has to be considered"

    elif templateNo == 2:
        # sizeof(body) >= number
        # python apriori_new.py -f association-rule-test-data.txt -s 0.5 -c 0.7 -t 2 -r sizeof-body-greaterthan-3
        ruleSplits = ruleTemplate.lower().split('-')
        _, noun, symbol, number = ruleSplits
        print noun, symbol, number
        if not noun in ['body', 'head', 'rule']:
            print noun + " not associated with the rule"
            return

        #convert number to int
        number = int(number)
        for rule, val in rule_with_val:
            body, head = rule
            if  noun == 'body':
                if len(body) >=  number:
                    generateAndPrintRule(rule, val)
    elif templateNo == 3:
        print "todo"
    else:
        print "please enter a valid template number and try again"
        return


def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        # file_iter = open(fname, 'rU')
        # for line in file_iter:
        with open(fname) as f:
            for line in f:
                words = line.split('\t')
                sample = set()
                for i in range(1, len(words) - 1): 
                    # leave the disease name
                    gene_structure = 'gene' + str(i) + '_' + words[i].lower()
                    sample.add(gene_structure)
                # adding disease
                diseasename = words[-1].replace('\n','')
                sample.add(diseasename)
                entry = frozenset(sample)
                if testing:
                    print diseasename
                    print entry
                yield entry



    


if __name__ == "__main__":

    par = OptionParser()
    par.add_option('-f', '--inputFile',dest='input',help='filename containing csv',default=None)
    par.add_option('-s', '--min_support', dest='minS',help='minimum support value', default=0.5,type='float')
    par.add_option('-c', '--min_conf',dest='minC',help='minimum confidence value',default=0.7,type='float')
    par.add_option('-t', '--templateNumber', dest='templateNo',help='give the template number',default=0,type='int')
    par.add_option('-r', '--rule',dest='rule',help='put one of the template rule defined in readme',default='no',type='string')

    (options, args) = par.parse_args()
    
    inFile = dataFromFile(options.input)
    # print "list from inFIle is "
    # print len(list(inFile))
    min_support = options.minS
    min_conf = options.minC
    ruleTemplate = options.rule
    templateNo = options.templateNo
    if testing:
        print ruleTemplate + ':' + str(templateNo)

    rule_with_val = calculateApriori(inFile, min_support, min_conf)
    # if result:
    #     printRules(rule_with_val)
    # testing template two
    # print "testing template two"
    # print "====================="
    # template2("RULE", 2, rule_with_val)
    # print "testing template one"
    # print "=========================="
    # template1("BODY", "ANY", ['gene59_up'], rule_with_val)
    # template1("BODY", "NONE", ['gene59_up'], rule_with_val)
    # template1("BODY", 2, ['gene59_up', 'gene32_down', 'gene1_down'], rule_with_val)
    # template1("RULE", "ANY", ['gene59_up'], rule_with_val)
    # template1("RULE", "NONE", ['gene59_up'], rule_with_val)
    # template1("RULE", 1, ['gene1_up', 'gene10_down'], rule_with_val)
    # template1("HEAD", "ANY", ['gene59_up'], rule_with_val)
    # template1("HEAD", "NONE", ['gene59_up'], rule_with_val)
    # template1("HEAD", 1, ['gene59_up', 'gene32_down', 'gene1_down'], rule_with_val)
    template3("1or1", "BODY", "ANY", ['Gene1_UP'], "HEAD", 1, ['Gene59_UP'], rule_with_val) #23
    # result, cnt = template1_helper("head", "none", ['gene1_up', 'gene10_down'], rule_with_val)
    # print result
    # print cnt

    # result, cnt = template2_helper("head", 2, rule_with_val)
    # print result
    # result, cnt = template1_helper("rule", 1, ['gene1_up', 'gene10_down'], rule_with_val)
    # print cnt
    # result, cnt = template1_helper("body", "any", ['gene1_up', 'gene10_down'], rule_with_val)
    # print 
    # result, cnt = template1_helper("body", "none", ['gene1_up', 'gene10_down'], rule_with_val)
    # print cnt
    # result, cnt1 = template1_helper("head", "any", ['gene1_up', 'gene10_down'], rule_with_val)
    # print cnt1
    # result, cnt = template2_helper("HEAD", 2, rule_with_val)
    # print result
    # print cnt





       