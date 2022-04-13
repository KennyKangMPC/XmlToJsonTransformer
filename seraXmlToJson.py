from xml.etree import ElementTree
import json

LISTTYPE = 1
DICTTYPE = 0

def getDictResults(res_dicts, iters):
    result_dicts = {}
    for iter in list(iters):
        iterxml(iter, result_dicts)

    if result_dicts:
        res_dicts[iters.tag].update(result_dicts)

def getListResults(res_dicts, iters):
    result_lists = []
    for iter in list(iters):
        result_dicts = {}
        iterxml(iter, result_dicts)
        result_lists.append(result_dicts.copy())
        del(result_dicts)
    
    if result_lists:
        if len(res_dicts[iters.tag].items()) == 0:
            res_dicts[iters.tag] = result_lists.copy()
        else:
            for resobj in result_lists:
                resobjkey = list(resobj.keys())[0]
                if res_dicts[iters.tag].get(resobjkey) == None:
                    res_dicts[iters.tag].update(resobj)
                else:
                    if type(res_dicts[iters.tag][resobjkey]) == list:
                        res_dicts[iters.tag][resobjkey].append(resobj[resobjkey].copy())
                    else:
                        old_value = res_dicts[iters.tag][resobjkey]
                        res_dicts[iters.tag][resobjkey] = []
                        res_dicts[iters.tag][resobjkey].append(old_value)
                        res_dicts[iters.tag][resobjkey].append(resobj[resobjkey].copy())

        del(result_lists)

def checkxmlchildrentype(iters):
    taglist = []
    for iter in list(iters): 
        taglist.append(iter.tag)

    if len(set(taglist)) == len(taglist):
        return DICTTYPE
    else:
        return LISTTYPE

def getResults(res_dicts, iters):
    if checkxmlchildrentype(iters):
        return getListResults(res_dicts, iters)
    else:
        return getDictResults(res_dicts, iters)

#@res_dicts    {}
def iterxml(iter, res_dicts):
    res_dicts[iter.tag] = {}

    if iter.attrib:
        for k,v in dict(iter.attrib).items():
            res_dicts[iter.tag].update({k : v})
    
    if iter.text is not None and iter.text.strip() != "":
        res_dicts[iter.tag].update({"__XmlTagText__" : iter.text.strip()})
    
    if list(iter): 
        getResults(res_dicts, iter)

def parserxmltojson(file_path):
    try:
        tree = ElementTree.parse(file_path)
    except Exception as e:
        #multi-byte encodings are not supported
        #encoding specified in XML declaration is incorrect
        #syntax error
        #not well-formed (invalid token)
        print("Parser {} Error, Errmsg: {}".format(file_path, e))
        return ""

    if tree is None:
        print("{} is None.".format(file_path))
        return ""

    root = tree.getroot()

    report = {}
    iterxml(root, report)
    #return getDictResults(root)

    return report

if __name__ == "__main__":
    jsonret = parserxmltojson("test.xml")
    with open("test.json", "w", encoding="utf-8") as fd:
        fd.write(json.dumps(jsonret, ensure_ascii=False, indent=4))
    print(json.dumps(jsonret, ensure_ascii=False, indent=4))