import requests
from bs4 import BeautifulSoup
from config import final_cnfg
from functions import autorisation
import math

question_types_dict = {0: "truefalse", 1: "multianswer", 2: "gapselect", 3: "calculated", 4: "shortanswer", 5: "multichoice", 6: "calculatedmulti",
                       7: "ddwtos", 8: "ddmarker", 9: "ddimageortext", 10: "calculatedsimple", 11: "randomsamatch", 12: "numerical", 13: "essay"}

session = requests.Session()
if not autorisation(session, final_cnfg['user']['login'], final_cnfg['user']['password'], final_cnfg["links"]['main_site']):
    print("ошибка авторизации")
    exit()


def forms_parser(session, block, counter):
    dict = {"No": counter, "type": block["class"][1]}

    def add_qtext():
        dict["qtext"] = block.find("div", {"class": "qtext"}).text

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
            print(x)

    match dict["type"]:
        case 'truefalse':
            add_qtext()
            set_answ(block.findAll("div", {"class": "r0"}), block.findAll(
                "div", {"class": "r1"}), "truefalse")
        case 'multianswer':
            pass
        case 'gapselect':
            pass
        case 'calculated':
            add_qtext()
        case 'multichoice':
            set_answ(block.findAll("div", {"class": "r0"}), block.findAll(
                "div", {"class": "r1"}))
            add_qtext()
        case 'calculatedmulti':
            add_qtext()
        case 'ddwtos':
            add_qtext()
        case 'ddmarker':
            add_qtext()
        case 'ddimageortext':
            add_qtext()
        case 'calculatedsimple':
            add_qtext()
        case 'shortanswer':
            add_qtext()
        case 'randomsamatch':
            add_qtext()
        case 'numerical':
            add_qtext()
        case 'essay':
            add_qtext()
    return dict


page_counter, test_url, prev_form, que_counter = 0, final_cnfg[
    "links"]['test_url']+'&page=', '', 0
while True:
    # получаем текст страницы
    page = BeautifulSoup(session.get(
        test_url+str(page_counter)).text, "html.parser")
    page_form = page.findAll(
        'form', {'id': 'responseform', 'enctype': 'multipart/form-data'})
    if page_form != prev_form:
        prev_form = page_form
        # находим форму с вопроссами
        # проверка на нахождение формы с вопроссами
        if page_form != []:
            blocks = page.findAll('div', {'class': 'que'})
            for que_block in blocks:
                print(forms_parser(session, que_block, que_counter))
                que_counter += 1
        else:
            print("блок вопроссов не найден")
    else:
        print("кол-во страниц:", page_counter)
        exit()
    page_counter += 1
