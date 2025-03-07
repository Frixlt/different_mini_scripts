import requests
from bs4 import BeautifulSoup
from config import final_cnfg
from functions import autorisation
from datetime import datetime

question_types_dict = {0: "truefalse", 1: "multianswer", 2: "gapselect", 3: "calculated", 4: "shortanswer", 5: "multichoice", 6: "calculatedmulti", 7: "ddwtos", 8: "ddmarker", 9: "ddimageortext", 10: "calculatedsimple", 11: "randomsamatch", 12: "numerical", 13: "essay"}

session = requests.Session()

def log():
    return datetime.now().strftime("%Y:%m:%d/%H:%M:%S") + "->"

if not autorisation(session, final_cnfg['user']['login'], final_cnfg['user']['password'], final_cnfg["links"]['main_site']):
    print(log(), "ошибка авторизации")
    exit()
else:
    print(log(), "авторизация успешна:")

def write_to_file(content, mode="a"):
    with open("result.txt", mode, encoding="utf-8") as file:
        file.write(content + "\n")

def forms_parser(session, block, counter):
    result_dict = {"No": counter, "type": block["class"][1]}
    return result_dict

def add_qtext(block):
    return block.find("div", {"class": "qtext"}).text

def set_answ(r0, r1, type=False):
    x, ans = False, []
    for i in range(len(r0) + len(r1)):
        if x:
            ans.append(r1[0])
            r1.remove(ans[-1])
            x = False
        else:
            ans.append(r0[0])
            r0.remove(ans[-1])
            x = True
    ret = []
    for i in ans:
        x = {}
        x["value"] = i.find("input").get("value")
        x["checked"] = True if i.find("input").get(
            "checked") == "checked" else False
        if type == "truefalse":
            pass
        else:
            x["answer"] = i.find("div", {"class": "flex-fill"}).text
        ret.append(x)
    return ret

# Write the initial prompt to the file
write_to_file('''
Ответь на вопросы теста, выбрав только правильный(правильные) вариант(варианты) ответа(ответов):
по шаблону:
%номер вопросса%) %правильный вариант ответа(если указанно что "возможно несколько правильных вариантов ответа" то перечисление через запятую)%
пример:
90) 2,4,5
91) 2
92) 2
Вопроссы:
''', mode="w")

page_counter, test_url, prev_form, que_counter = 0, final_cnfg[
    "links"]['test_url']+'&page=', '', 0

while True:
    page = BeautifulSoup(session.get(
        test_url+str(page_counter)).text, "html.parser")
    page_form = page.findAll(
        'form', {'id': 'responseform', 'enctype': 'multipart/form-data'})
    if page_form != prev_form:
        prev_form = page_form
        if page_form != []:
            blocks = page.findAll('div', {'class': 'que'})
            for que_block in blocks:
                result_dict = forms_parser(session, que_block, que_counter)
                que_counter += 1
                print(log(), "парсинг страницы:",que_counter)
                match result_dict["type"]:
                    case 'truefalse':
                        qtext = add_qtext(que_block)
                    case 'multianswer':
                        pass
                    case 'gapselect':
                        pass
                    case 'calculated':
                        qtext = add_qtext(que_block)
                    case 'multichoice':
                        output = f"Вопросс {que_counter}:"
                        if que_block.find('div', {'class': 'answer'}).find_all("input", {"type": "checkbox"}):
                            output += " (возможно несколько правильных вариантов ответа)"
                        else:
                            output += " (только один правильный вариант ответа)"
                        output += f"\n{que_block.find('div', {'class': 'qtext'}).text}\n"
                        for x, i in enumerate(set_answ(que_block.findAll("div", {"class": "r0"}), que_block.findAll(
                                "div", {"class": "r1"}))):
                            output += f"{x+1}) {i['answer']}\n"
                        output+="\n"
                        write_to_file(output)
                    case 'calculatedmulti':
                        qtext = add_qtext(que_block)
                    case 'ddwtos':
                        qtext = add_qtext(que_block)
                    case 'ddmarker':
                        qtext = add_qtext(que_block)
                    case 'ddimageortext':
                        qtext = add_qtext(que_block)
                    case 'calculatedsimple':
                        qtext = add_qtext(que_block)
                    case 'shortanswer':
                        qtext = add_qtext(que_block)
                    case 'randomsamatch':
                        qtext = add_qtext(que_block)
                    case 'numerical':
                        qtext = add_qtext(que_block)
                    case 'essay':
                        qtext = add_qtext(que_block)
        else:
            print("блок вопроссов не найден")
    else:
        print(log(), "промт сформирован")
        exit()
    page_counter += 1