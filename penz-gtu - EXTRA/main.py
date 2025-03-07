import requests
from bs4 import BeautifulSoup
from config import final_cnfg
# создаем словарь для хранения вопроссов
dict = {}
# получаем из конфига url сайта
url = final_cnfg["links"]['main_site']
# запускаем ссесию
session = requests.Session()
# получаем токен авторизации
page = session.get(url)
soup = BeautifulSoup(page.text, "html.parser")
logintoken = soup.find('input', {'name': 'logintoken'}).get('value')
# попытка входа в акаунт
post_request = session.post(url, {
    'logintoken': logintoken,
    'username': 's000009649',
    'password': '50815081m',
})

# проверка вошли ли мы?
soup = BeautifulSoup(post_request.text, "html.parser")
if soup.findAll('div', {'class': 'alert alert-danger', 'role': 'alert'}) == []:
    print('авторизация прошла успешно!')
    # начинаем проходиться по всем страницам с вопроссами
    page_counter, test_url, prev_form = 0, final_cnfg["links"]['test_url']+'&page=', ''
    while True:
        # получаем текст страницы
        page = BeautifulSoup(session.get(
            test_url+str(page_counter)).text, "html.parser")
        page_form = page.findAll(
            'form', {'id': 'responseform', 'enctype': 'multipart/form-data'})
        # если наша страница совпадает с предыдущей то значит мы вытащили все вопроссы => завершаем цикл
        if page_form != prev_form:
            prev_form = page_form
            # находим форму с вопроссами
            # проверка на нахождение формы с вопроссами
            if page_form != []:
                page_form = page_form[0]
                # ищем блоки вопроссов
                question_bocks = page_form.findAll('div', {'class': 'que'})
                # проходимся по каждому блоку
                for question_bock in question_bocks:
                    # получаем номер вопросса
                    question_number = question_bock.findAll(
                        'span', {'class': 'qno'})
                    if question_number != []:
                        question_number = question_number[0].text
                    else:
                        question_number = "номер вопросса не найден(class qno)"
                    # уникальный id вопросса
                    question_id = question_bock.get('id')
                    # текст самого вопросса
                    question = question_bock.findAll('div', {'class': 'qtext'})
                    if question != []:
                        question = question[0].text
                    else:
                        question = "текст вопросса не найден"
                    # тут будет реалитзация поиска типа вопросса answer_type
                    answer_full_block = question_bock.findAll(
                        attrs={'class': 'answer'})
                    if answer_full_block != []:
                        # вытаксиваем имя тэга в котором расположен class answer
                        match answer_full_block[0].name:
                            case "div":
                                # определяем это вопросс со множественным выбором или с 1
                                if answer_full_block[0].findAll(type="radio") != []:
                                    # тип вопросса - 1 вариант
                                    answer_type = "one"
                                elif answer_full_block[0].findAll(type="checkbox") != []:
                                    # тип вопросса - несколько правильных вариантов
                                    answer_type = "many"
                                else:
                                    print(
                                        "ошибка в определении типа вопросса (не checkbox и не radio)")
                            case "span":
                                # тип вопросса - поле для ввода
                                answer_type = "input"
                            case _:
                                print("неизвестный тип:",
                                      answer_full_block[0].name)
                    else:
                        print("ошибка, (class answer) не найден")
                    # если пристутсвуют несколько вариантов ответов то:
                    if answer_type != "input":
                        # создаем список для наполнения вариантами ответов
                        answers = []
                        # ищем блоки вопроссов
                        answers_block = question_bock.findAll(
                            'div', {'data-region': 'answer-label'})
                        # проходимся циклом по каждому блоку вопроссов
                        count_answer = 0
                        for answer in answers_block:
                            # извлекаем текст вопросса
                            result_line = ""
                            answer = answer.findAll('p')
                            for lines in answer:
                                result_line += lines.text
                            # проверяем не отмечен ои этот вариант как ответ
                            count_answer += 1
                            answers.append([result_line])
                        # закидываем в словарь полученные данные
                        dict[question_number] = {
                            "answer_type": answer_type, "question": question, "answers": answers}
                    else:
                        pass
            else:
                # save(page.text)
                print('форма с вопроссами не найдена')
                exit()
        else:
            print("всего страниц:", page_counter)
            break
        page_counter += 1
else:
    print('ошибка', end=': ')
    print(soup.findAll(
        'div', {'class': 'alert alert-danger', 'role': 'alert'})[0].text)
print(dict)
