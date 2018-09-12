import random
import decimal
import math
import time


class Assessment:
    def __init__(self):
        self.section1 = {}
        self.section2 = {}
        self.section3 = {}

        self.history = []

        self._init_questions()

    def assess(self, section=None):
        """ This runs the test. Choose section or leave it at None to do the full test. """

        print('wait 5 secs')
        time.sleep(5)
        self.history = []
        print('Starting test...')
        start_time = time.time()
        points = 0

        if section is None or section == 1:
            print('Section 1')
            for i, q in enumerate(self.section1['questions']):
                res = self._ask_question(q, self.section1['answers'][i], 1)
                if res is not None:
                    points += 1 if res else -3

            section1_end_time = time.time()
            section1_time = section1_end_time - start_time
            print('Section 1 took {:.1f}s'.format(section1_time))
            print('Points: {} / 30'.format(points))
            section1_points = points

        if section is None or section == 2:
            print('Section 2')
            for i, q in enumerate(self.section2['questions']):
                res = self._ask_question(q, self.section2['answers'][i], 2)
                if res is not None:
                    points += 2 if res else -1

            section2_end_time = time.time()

            if section is None:
                section2_time = section2_end_time - section1_end_time
                print('Section 2 took {:.1f}s... test so far took {:.1f}s'.format(section2_time, section2_end_time - start_time))
                print('Points: {} / 60'.format(points - section1_points))
                print('Total points: {} / 90'.format(points))
                section2_points = points
            else:
                print('Test took {:.1f}s'.format(section2_end_time - start_time))
                print('Points: {} / 60'.format(points))

        if section is None or section == 3:
            print('Section 3')
            for i, q in enumerate(self.section3['questions']):
                res = self._ask_question(q, self.section3['answers'][i], 3, choices=self.section3['choices'][i])
                if res is not None:
                    points += 2 if res else -2

            end_time = time.time()

            if section is None:
                section3_time = end_time - section2_end_time
                print('Section 3 took {:.1f}s... test took {:.1f}s'.format(section3_time, end_time - start_time))
                print('Points: {} / 30'.format(points - section2_points))
                print('Total points: {} / 120'.format(points))
                print('Test passed' if points >= 72 else 'Test failed')
            else:
                print('Test took {:.1f}s'.format(end_time - start_time))
                print('Points: {} / 60'.format(points))

        self.print_history()

    def print_history(self):
        sect = 0
        correct_count = 0
        valid_q_count = 0
        tot_time = 0

        for i, q in enumerate(self.history):
            if q['section'] > sect:
                sect = q['section']
                print('Section {}'.format(sect))

            if q['correct'] is not None:
                tot_time += q['time']
                valid_q_count += 1
                correct_count += 1 if q['correct'] else 0

            # this is just a filter if you don't want every question printed. Uncomment the if statement to only return
            # wrong answers and bad questions
            qualifier = True #if (q['correct'] is None or not q['correct']) else False

            if qualifier:
                print('{}| Correct: {} | Time: {:.1f} | Q: {} | A: {} | Given A: {}'.format(
                    i, q['correct'], q['time'], q['question'], q['answer'], q['user answer']))

        print('{} / {} questions answered correctly'.format(correct_count, valid_q_count))
        print('Total test time: {:.1f}s, Average question time: {:.1f}s'.format(tot_time, tot_time / valid_q_count))

    def _ask_question(self, question, answer, section, choices=None):

        question_start_time = time.time()

        if section < 3:
            user_answer = input(question + ' = ')

            # bad question flag -  it will ignore the question in the results if you answer with 'o'
            if user_answer != 'o':
                user_answer = float(user_answer)
        else:
            random.shuffle(choices)
            print(question)
            print(choices)
            user_answer = choices[int(input('1, 2 or 3: ')) - 1]

        time_taken = time.time() - question_start_time

        if not isinstance(user_answer, str):
            result = math.isclose(user_answer, answer, abs_tol=1e-5)
        else:
            result = None

        self.history.append({
            'section': section,
            'correct': result,
            'question': question,
            'user answer': user_answer,
            'answer': answer,
            'time': time_taken
        })

        return result

    def _init_questions(self):
        """ Generates questions for all sections """

        # section 1 - simple questions
        questions = []
        answers = []
        for i in range(30):
            op = random.choice(['-', '+', '*', '/'])

            if op == '/' or op == '*':
                v1 = random.randint(1, 12)
                v2 = random.randint(1, 99)
                if op == '/':
                    answ = v1 * v2
                    v2 = v1
                    v1 = answ
            else:
                v1 = random.randint(1, 99)
                v2 = random.randint(1, 199)

            question = '{} {} {}'.format(v1, op, v2)
            answ = eval(question)
            questions.append(question)
            answers.append(answ)
            self.section1 = {'questions': questions, 'answers': answers}

        # section 2 - harder questions with decimals
        # based off https://www.flowtraders.com/sites/default/files/inline-files/arithmetic_test_example.pdf
        # just randomising these questions slightly because it's all the info I have
        questions = []
        answers = []

        questions.append(self.section2_question_gen(0.5, '*', 0.5, 1, 1, 0.5, 0.5))
        questions.append(self.section2_question_gen(0.002, '*', 40, 1, 0, 0.01, 10))
        questions.append(self.section2_question_gen(0.6, '/', 15, 1, 0, [0.6, 1.2, 0.06], [15, 20, 30, 1.5, 12, 1.2]))
        questions.append(self.section2_question_gen(0.1, '-', 0.04, 2, 1, 2, 0.08))
        questions.append(self.section2_question_gen(0.012, '*', 40, 2, 0, 0.01, [20, 30, 40, 50, 60]))

        questions.append(self.section2_question_gen(22200, '*', 0.003, 0, 1, [22200, 11110, 12300], 0.003))
        questions.append(self.section2_question_gen(0.3, '/', 0.01, 1, 1, 10, [0.001, 0.01, 0.1]))
        questions.append(self.section2_question_gen(2.5, '*', 0.04, 2, 1, 2.4, 0.04))
        questions.append(self.section2_question_gen(0.990, '+', 1.03, 4, 3, 0.009, 0.29))
        questions.append(self.section2_question_gen(3.03, '-', 0.11, 3, 2, 0.09, 0.09))

        questions.append(self.section2_question_gen(6, '*', 1.25, 0, 2, 4, [1.25, 1.5, 1.75]))
        questions.append(self.section2_question_gen(18, '/', 1.2, 0, 2, [18, 15], [1.2, 1.5]))
        questions.append(self.section2_question_gen(0.08, '*', 2.5, 1, 2, 0.07, 5))
        questions.append(self.section2_question_gen(5287, '+', 3658, 0, 0, 1000, 1000))
        questions.append(self.section2_question_gen(11.07, '-', 9.18, 4, 3, 0.09, 0.9))

        questions.append(self.section2_question_gen(15, '/', 0.4, 0, 2, [15, 20, 10, 25], [0.2, 0.4, 0.8]))
        questions.append(self.section2_question_gen(0.01, '/', 0.1, 1, 1, [0.01, 0.1, 0.04, 0.4], [0.1, 0.01, 0.2, 0.02]))
        questions.append(self.section2_question_gen(0.04, '*', 5.5, 1, 2, 0.04, 4))
        questions.append(self.section2_question_gen(55.28, '+', 1.338, 4, 4, 2, 1))
        questions.append(self.section2_question_gen(55.338, '-', 0.889, 5, 3, 2, 0.5))

        questions.append(self.section2_question_gen(-4.66, '+', 2.555, 3, 4, 4, 2))
        questions.append(self.section2_question_gen(0.12, '/', 6, 2, 0, [0.12, 0.24, 0.36], [2, 6, 3]))
        questions.append(self.section2_question_gen(14, '/', 0.7, 5, 4, [14, 28, 42], [0.7, 0.14]))
        questions.append(self.section2_question_gen(80, '*', 1.02, 0, 3, 50, 0.08))
        questions.append(self.section2_question_gen(6.44, '*', 0.25, 5, 0, [6.52, 3.8, 14.48, 6.08], [0.25, 0.5]))

        questions.append(self.section2_question_gen(8769, '+', 3654, 0, 0, 2000, 2000))
        questions.append(self.section2_question_gen(0.75, '*', 0.3, 2, 1, 5, 5))   # the one on the sheet is a typo
        questions.append(self.section2_question_gen(11, '*', 0.002, 0, 1, 10, 0.008))
        questions.append(self.section2_question_gen(77.66, '*', 0.5, 4, 0, 50, 0))
        questions.append(self.section2_question_gen(5.4, '*', 0.15, 2, 0, 5, [0.15, 0.25, 0.35, 0.05]))

        random.shuffle(questions)

        for q in questions:
            answers.append(eval(q))

        self.section2 = {'questions': questions, 'answers': answers}


        # section 3 - multiple choice
        # don't have much info on this at all so it's a guess

        questions = []
        answers = []
        multi_choice = []

        for i in range(15):
            v1 = random.randint(101, 9999)
            v2 = random.randint(101, 9999)
            op = '*'
            question = '{} {} {}'.format(v1, op, v2)
            questions.append(question)
            answ = eval(question)
            answers.append(answ)
            multi_choice.append([answ, self.section3_answer_gen(answ), self.section3_answer_gen(answ)])
        self.section3 = {'questions': questions, 'answers': answers, 'choices': multi_choice}


    def section2_question_gen(self, v1, op, v2, sf1, sf2, lim1, lim2):
        """
        eval(question)
        :param v1: variable 1
        :param op: operation
        :param v2: variable 2
        :param sf1: number of sig figs for variable 1 (0 means integers only)
        :param sf2: number of sig figs for variable 2 (0 means integers only)
        :param lim1: limit of fluctuation for variable 1 (this can also be a list of variables to choose from)
        :param lim2: limit of fluctuation for variable 2 (this can also be a list of variables to choose from)
        :return: randomised question
        """
        if isinstance(lim1, list):
            v1 = random.choice(lim1)
        elif sf1 > 0:
            decimal.getcontext().prec = sf1
            v1 = decimal.Decimal(v1) + decimal.Decimal((random.random() - 0.1) * lim1)
        elif sf1 == 0:
            v1 += random.randint(-lim1, lim1)

        if isinstance(lim2, list):
            v2 = random.choice(lim2)
        elif sf2 > 0:
            decimal.getcontext().prec = sf2
            v2 = decimal.Decimal(v2) + decimal.Decimal((random.random() - 0.1) * lim2)
        else:
            v2 += random.randint(-lim2, lim2)

        return '{} {} {}'.format(v1, op, v2)

    def section3_answer_gen(self, answer):
        """ generates some close but wrong answers """
        var = 0
        while var == 0:
            var = random.randint(-10, 10)

        return random.choice([answer + 10 * var, answer+var])


if __name__ == '__main__':

    assessment = Assessment()
    try:
        assessment.assess(section=None)
    except Exception as e:
        print(e)
        print(assessment.history)