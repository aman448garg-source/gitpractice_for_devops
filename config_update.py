import sys, os, re, os.path, shutil
import argparse, sys

parser=argparse.ArgumentParser()
#2.4
parser.add_argument('--current', help='Current cofig folder path')
parser.add_argument('--new', help='New config folder path')
parser.add_argument('--output', help='output folder')
parser.add_argument('--type', help='xml or nonxml')

args = parser.parse_args()
to_copy_folder = ['app']
to_ignore = ['.xsd']
#print(args.current)
#test_dir = [i for i in os.listdir(args.current)]
#for dir in test_dir:
#  if os.path.isdir(args.current + dir):
#    os.system("cp -R "+args.current+dir+"/ " +args.output)
if not args.type == 'xml':
    files_1 = []
    for i in os.listdir(args.current):
        if os.path.isdir(os.path.join(args.current, i)):
            for item in sys.argv:
                if "--current" in item:
                    current_path = item.split("=")[1]
                if "--new" in item:
                    new_path = item.split("=")[1]
                if "--out" in item:
                    output_path = item.split("=")[1]
            if not os.path.exists(os.path.join(output_path, i)):
                os.makedirs(os.path.join(output_path, i))
            os.system("python3 config_update.py --current=%s --new=%s --output=%s --type=nonxml" % (
                    os.path.join(current_path, i),
                    os.path.join(new_path, i),
                    os.path.join(output_path, i)
                )
            )
            continue
        if not '.xml' in i:
            files_1.append(i)




    # files_1 = [i for i in os.listdir(args.current) if not '.xml' in i]
    files_2 = [i for i in os.listdir(args.new) if not '.xml' in i]
    for file_name in files_1:
      print(file_name)
      if os.path.isdir(args.current + "/" + file_name):
        if file_name == "examples":
           continue
        else:
           pass
#           os.system("cp -Rf " + args.current + "/" + file_name + "/ " + args.output)
      else:
        if not file_name in files_2:
            print("missing file %s in new folder" % file_name)
            os.system("cp -Rf " + args.current + "/" + file_name + " " + args.output)
            # with open(os.path.join(args.output, file_name), 'w') as outfile:
            #     with open(os.path.join(args.current, file_name)) as infile:
            #         outfile.write(infile.read())
            continue
        with open(os.path.join(args.new, file_name)) as f2:
            whole_data = f2.readlines()
            #aug_3
            if "".join(whole_data).count(":") > "".join(whole_data).count("="):
                seperator = ":"
            else:
                seperator = "="
            #aug_3
            lines_2 = []  
            for i in whole_data:
                if i.startswith('#') or not i.strip():
                    continue
                else:
                    if seperator in i:
                        lines_2.append([j.strip() for j in i.strip().split(seperator)])
                    else:
                        lines_2.append(i.strip())

        with open(os.path.join(args.current, file_name)) as f1:
            lines_1 = []
            #aug_3
            whole_data = f1.readlines()
            if "".join(whole_data).count(":") > "".join(whole_data).count("="):
                seperator = ":"
            else:
                seperator = "="
            #aug_3
            for i in whole_data:
                if i.startswith('#') or not i.strip():
                    continue
                else:
                    if seperator in i:
                        lines_1.append([j.strip() for j in i.strip().split(seperator)])
                    else:
                        lines_1.append(i.strip()) 


        with open(os.path.join(args.output, file_name), 'w') as f3:
            with open(os.path.join(args.current, file_name)) as f1:
                f3.write(f1.read())
                if any([i in file_name for i in to_ignore]):
                    continue
                f3.write("\n\n\n################ CONFIGS ADDED ################\n\n")
                for i in lines_2:
                    print(i)
                    if isinstance(i,str):
                      if "=" in i:
                        i=i.split("=")
                      if ":" in i:
                        i=i.split(":")
                    found = False
                    for j in lines_1:
                        if "=" in j:
                           j=j.split("=")
                        if ":" in j:
                           j=j.split(":")
                        if isinstance(i, list):
                            if isinstance(j, list):
                                if i[0] == j[0]:
                                    found = True
                        else:
                            if isinstance(j, str):
                                if i == j:
                                    found = True
                    print(found)
                    if not found:
                        if isinstance(i, list):
                            f3.write((seperator or " = ").join(i))
                        else:
                            f3.write(i)
                        f3.write("\n")
                f3.write("\n################ END CONFIGS ADDED ################n")

    for file_name in files_2:
      if os.path.isdir(args.new +"/"+ file_name):
        #os.system("cp -Rf "+args.new+"/"+file_name+"/ " +args.output)
        continue
      else:
        if not file_name in files_1:
          print("missing file %s in current folder" % file_name)
          os.system("cp -Rf " + args.new + "/" + file_name + " " + args.output)
          # with open(os.path.join(args.output, file_name), 'w') as outfile:
          #     with open(os.path.join(args.new, file_name)) as infile:
          #         outfile.write(infile.read())
          continue
    for i in os.listdir(args.new):
        if os.path.isdir(os.path.join(args.new, i)):
            if not os.path.exists(os.path.join(args.output, i)):
                from distutils.dir_util import copy_tree
                copy_tree(os.path.join(args.new, i), os.path.join(args.output, i))

    for i in os.listdir(args.output):
        if i in to_copy_folder:
            os.system("cp " + os.path.join(args.output, "%s/sig-firewall-SIP*" % i) + " " + os.path.join(args.output))
            os.system("cp " + os.path.join(args.output, "%s/sig-firewall-gtp*" % i) + " " + os.path.join(args.output))
else:
    def _xpath(tree, path):
        try:
            return tree.xpath(path) or [type('A', (), {'tag': type('B', (), {'title': dict})})]
        except:
            # path = "/"+"/".join(path.split("/")[:1] + path.split("/")[2:])
            path = "/".join([('*' if ':' in k else k) for k in (path.split("/"))])
            return tree.xpath(path) or [type('A', (), {'tag': type('B', (), {'title': dict})})]
    from xmldiff import main
    from lxml import etree
    from xmldiff.patch import Patcher
    import xml.dom.minidom
    import os
    from xmldiff import actions


    files_1 = []
    for i in os.listdir(args.current):
        if os.path.isdir(os.path.join(args.current, i)):
            for item in sys.argv:
                if "--current" in item:
                    current_path = item.split("=")[1]
                if "--new" in item:
                    new_path = item.split("=")[1]
                if "--out" in item:
                    output_path = item.split("=")[1]
            if not os.path.exists(os.path.join(output_path, i)):
                os.makedirs(os.path.join(output_path, i))
            os.system("python3 config_update.py --current=%s --new=%s --output=%s --type=xml" % (
                    os.path.join(current_path, i),
                    os.path.join(new_path, i),
                    os.path.join(output_path, i)
                )
            )
            continue
        if  '.xml' in i:
            files_1.append(i)


    #files_1 = [i for i in os.listdir(args.current) if '.xml' in i]
    files_2 = [i for i in os.listdir(args.new) if '.xml' in i]
    for file_name in files_1:
        print("FILE: ", file_name)
        if not file_name in files_2:
            print("missing file %s in new folder" % file_name)
            os.system("cp -Rf " + args.current + "/" + file_name + " " + args.output)
            # with open(os.path.join(args.output, file_name), 'w') as outfile:
            #     with open(os.path.join(args.current, file_name)) as infile:
            #         outfile.write(infile.read())
            continue
        try:
            patcher = Patcher()

            tree = etree.parse(os.path.join(args.new, file_name))

            diffs = main.diff_files(os.path.join(args.new, file_name), os.path.join(args.current, file_name))
            diffs = [i for i in diffs if not 'schemaLocation' in str(i)] #18-04
            new_nodes = []
            to_delete = []
            for i in diffs:
                print("++++", i)
                try:
                    tree = patcher.patch([i], tree)
                except Exception as e: print(e)


            #######

                if "InsertNode" in str(i):
                    to_delete.append(i.tag)

            for i in to_delete:
                print(i)
                try:
                    xpath = "//*[local-name() = '%s']" % i.split("}")[-1]
                    new = etree.parse(os.path.join(args.new, file_name))
                    if not new.xpath(xpath):
                        tree = patcher.patch([actions.DeleteNode(xpath)], tree)
                except: pass



            #########

            dom = xml.dom.minidom.parseString(etree.tostring(tree, xml_declaration=False))
            pretty_xml_as_string = dom.toprettyxml()
            with open(os.path.join(args.output, file_name), 'w') as f3:
                with open(os.path.join(args.new, file_name)) as orig:
                    lines = [i for i in orig.readlines()]
                    f3.write(os.linesep.join([s for s in pretty_xml_as_string.splitlines()
                                                  if s.strip()]))




            continue
            tree = etree.parse(os.path.join(args.output, file_name))
            diffs = main.diff_files(os.path.join(args.output, file_name), os.path.join(args.current, file_name))
            diffs = [i for i in diffs if not 'schemaLocation' in str(i)] #18-04
            to_delete = []
            for i in diffs:
                print("===",i)
                if "InsertNode" in str(i):
                    to_delete.append(i.tag)
                    #import pdb; pdb.set_trace()
                # if not "UpdateTextIn" in str(i) and not "UpdateAttrib" in str(i):
                #     continue
                tree = patcher.patch([i], tree)

            for i in to_delete:
                print(i)
                try:
                    xpath = "//*[local-name() = '%s']" % i.split("}")[-1]
                    new = etree.parse(os.path.join(args.new, file_name))
                    if not new.xpath(xpath):
                        tree = patcher.patch([actions.DeleteNode(xpath)], tree)
                except: pass


            dom = xml.dom.minidom.parseString(etree.tostring(tree, xml_declaration=False))
            pretty_xml_as_string = dom.toprettyxml()
            with open(os.path.join(args.output, file_name), 'w') as f3:
                with open(os.path.join(args.current, file_name)) as orig:
                    lines = [i for i in orig.readlines()]
                    pretty_lines = pretty_xml_as_string.splitlines()
                    
                    to_add = None
                    for i in lines[:5]:
                        if "xml version" in i:
                            to_add = i
                            for j in pretty_lines[:5]:
                                if "xml version" in j:
                                    pretty_lines.remove(j)
                                    #to_add = False
                    if to_add:
                        f3.write(to_add)
                    to_add = None
                    for i in lines[:5]:
                        if "!DOCTYPE" in i:
                            to_add = i
                            for j in pretty_lines[:5]:
                                if "!DOCTYPE" in j:
                                    pretty_lines.remove(j)
                    if to_add:
                        f3.write(to_add)
                    f3.write(os.linesep.join([s for s in pretty_lines if s.strip()]))





            #     # skip = False
            #     if "DeleteNode" in str(i) or "InsertComment" in str(i):
            #         continue
            #     print(i)

            #     # elif "InsertNode" in str(i):

            #     #     for j in _xpath(tree, i.target)[0].getchildren():
            #     #         if j.tag == i.tag:
            #     #             to_delete.append("%s/*[%s]" % (i.target, i.position + 1))
            #     #             skip = True
            #     #             break
            #     #     else:
            #     #         new_nodes.append(i.tag.title())
            #     # else:
            #     #     try:
            #     #         if not _xpath(tree, getattr(i, "node", None) or getattr(i, "target", None))[0].tag.title() in new_nodes:
            #     #             continue
            #     #     except:
            #     #         pass
            #     # if skip:
            #     #     continue
            #     if "MoveNode" in str(i):
            #         tree = patcher.patch([i], tree)
            #         continue
            #     # if "UpdateTextIn" in str(i) and (not _xpath(tree, getattr(i, "node", None) or getattr(i, "target", None))[0].tag.title() in new_nodes):
            #     #     continue

            #     if "InsertNode" in str(i):
            #         path = "/".join([('*' if ':' in k else k) for k in (i.target.split("/") + [re.sub('{.+}' ,'', i.tag)])])
            #         t1 = etree.parse(os.path.join(args.current, file_name))
            #         t2 = etree.parse(os.path.join(args.new, file_name))
            #         print(len(t1.xpath(path)),len(t2.xpath(path)), path)
            #         #aug_4
            #         if not len(t1.xpath(path)) and not len(t2.xpath(path)):
            #             path = path.replace(re.sub('{.+}' ,'', i.tag), '*[contains(name(), "%s")]' % re.sub('{.+}' ,'', i.tag))
            #         #aug_4
            #         print(len(t1.xpath(path)),len(t2.xpath(path)), path)
            #         if len(t1.xpath(path)) != len(t2.xpath(path)):
            #             new_nodes.append(i.tag.title())
            #         else:
            #             pass
            #             #continue #aug_3
            #     elif (not _xpath(tree, getattr(i, "node", None) or getattr(i, "target", None))[0].tag.title() in new_nodes): #aug_3
            #         print(4444)
            #         continue #aug_3
            #     if ":" in getattr(i, "node", "") or ":" in getattr(i, "target", ""):
            #         print(11111)
            #         cl = i.__class__
            #         data = i._asdict()
            #         if "node" in data:
            #             data['node'] = re.sub('\\w+:\\w+' ,'*', data['node'])
            #         if "target" in data:
            #             data['target'] = re.sub('\\w+:\\w+' ,'*', data['target'])
            #         i = cl(**data)
            #         if "InsertAttrib" in str(i):
            #             try:
            #                 tree = patcher.patch([i], tree)
            #             except:
            #                 pass
            #         else:
            #             tree = patcher.patch([i], tree)
            #     else:
            #         print(222)
            #         if "InsertAttrib" in str(i):
            #             try:
            #                 tree = patcher.patch([i], tree)
            #             except:
            #                 pass
            #         else:
            #             print(3333)
            #             tree = patcher.patch([i], tree)
            # tree = patcher.patch([actions.DeleteNode(i) for i in to_delete], tree)
            # try:
            #     with open(os.path.join(args.output, file_name), 'w') as f3:
            #         #f3.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding=tree.docinfo.encoding).decode())
            # f3.write(etree.tostring(tree, xml_declaration=True, doctype=tree.docinfo.doctype, encoding=tree.docinfo.encoding, inclusive_ns_prefixes=tree.getroot().nsmap, pretty_print=True).decode())
            # except Exception as e:
            #     print(e)
            # dom = xml.dom.minidom.parseString(etree.tostring(tree))
            # pretty_xml_as_string = dom.toprettyxml()
            # with open(os.path.join(args.output, file_name), 'w') as f3:
            #     with open(os.path.join(args.new, file_name)) as orig:
            #         lines = [i for i in orig.readlines()]
            #         for i in lines[:5]:
            #             if "xml version" in i:
            #                 f3.write(i)
            #                 break
            #         for i in lines[:5]:
            #             if "!DOCTYPE" in i:
            #                 f3.write(i)
            #                 break
            #         f3.write(os.linesep.join([s for s in pretty_xml_as_string.splitlines()
            #                                       if s.strip()]))
        except:
            print("ERROR: %s" % file_name)
            import traceback
            print(traceback.format_exc())
    for file_name in files_2:
        if not file_name in files_1:
            print("missing file %s in current folder" % file_name)
            os.system("cp -Rf " + args.new + "/" + file_name + " " + args.output)
            # with open(os.path.join(args.output, file_name), 'w') as outfile:
            #     with open(os.path.join(args.new, file_name)) as infile:
            #         outfile.write(infile.read())
            continue
    for i in os.listdir(args.new):
        if os.path.isdir(os.path.join(args.new, i)):
            if not os.path.exists(os.path.join(args.output, i)):
                from distutils.dir_util import copy_tree
                copy_tree(os.path.join(args.new, i), os.path.join(args.output, i))

    for i in os.listdir(args.output):
        if i in to_copy_folder:
            os.system("cp " + os.path.join(args.output, "%s/sig-firewall-SIP*" % i) + " " + os.path.join(args.output))
            os.system("cp " + os.path.join(args.output, "%s/sig-firewall-gtp*" % i) + " " + os.path.join(args.output))
























            
            
