# TODO
0. local evaluation  
1. simple routing for problems 1-5. astar isnt fast enough (my implementation) so i cant deliver all orders, rovers dont pay off
2. chains of orders, so rover can take next order faster and without idling
3. astar heuristic optimization for city (problems 6-10)
4. caching tracks between quadrants for large number of orders it can save a lot of computations

# ysdc_contest
202109 contest on dispatching rovers https://contest.yandex.ru/contest/28643


A. Роботы-курьеры
Ограничение времени 	20 секунд
Ограничение памяти 	1Gb
Ввод 	стандартный ввод
Вывод 	стандартный вывод

В Иннополисе уже давно наступило будущее, и доставка заказа из кафе человеком - скорее редкость, чем правило. Большинство заказов в городе доставляют роботы-курьеры, и в этой задаче мы предлагаем вам поучаствовать в распределении роботов по заказам, происходящим в течение некоторого времени.

Представим город в виде карты размера N × N. Для простоты предположим, что робот занимает ровно одну клетку и каждая клетка для него может быть либо проходимой, либо нет. За одну секунду робот может переместиться в любом из четырёх направлений (вверх/вниз/влево/вправо), если клетка, куда он хочет переместиться, свободна.

В начале теста вам нужно вывести количество роботов, которое вы хотите использовать для доставки заказов, и их изначальные координаты. Постройка каждого робота будет стоить Costc рублей.

Далее будет произведено T итераций симуляции. Одна итерация представляет собой одну виртуальную минуту и состоит из 60 секунд. На каждой итерации вашей программе будет передано количество новых заказов, а в ответ программа должна сообщить, какие действия выполняет каждый робот (по 60 действий для робота).

За каждый успешно доставленный заказ вы получите max(0, MaxTips - DeliveryTime) рублей чаевых, где MaxTips — максимальное количество чаевых для одного заказа, а DeliveryTime — время с момента появления заказа до его доставки в секундах.

Итоговое количество очков, которое вы заработаете за один тест вычисляется по формуле TotalTips - R× Costc, где TotalTips — общее количество заработанных чаевых, R — количество использованных роботов, Costc — цена постройки одного робота. Значения Costc и MaxTips задаются в каждом тесте. Если вы заработали меньше чаевых, чем потратили на производство роботов, итоговое количество очков будет равно 0. Также вы получите 0 очков за тест в случае выполнения любого некорректного действия.
Формат ввода

Для чтения входных данных программа должна использовать стандартный ввод.

В первой строке ввода заданы три натуральных числа N, MaxTips и Costc (N ≤ 2 000, MaxTips≤ 50 000, Costc≤ 109) — размер города, максимальное количество чаевых за заказ и цена постройки одного робота. Каждая из следующих N строк содержит N символов — карту города. Строки могут содержать два типа символов:

    '#' - клетка занята препятствием.
    '.' - свободное пространство.

Затем вам на вход будет подано два целых натуральных числа T и D (T ≤ 100 000, D ≤ 10 000 000) — количество итераций взаимодействия и суммарное количество заказов.

После этого вам необходимо вывести число R - количество роботов, которые вы разместите в городе. Роботов должно быть не менее, чем 1 и не более, чем 100. Затем выведите R пар целых чисел от 1 до N — координаты, где роботы будут изначально расположены.

Далее на каждой из T итераций мы сообщаем информацию о новых размещенных заказах. На каждой итерации сначала дано целое число k — количество новых курьерских заказов, затем k строк с числами Srow, Scol, Frow, Fcol — координаты начальной и конечной точки заказа (1 ≤ Srow, Scol, Frow, Fcol ≤ N). Новый заказ может быть размещён в той же клетке, где уже находится 1 или более заказов. Время жизни заказа не ограничено.
Формат вывода

Для осуществления запросов программа должна использовать стандартный вывод.

На каждой итерации в ответ вы сообщаете нам о действиях каждого из своих роверов: R строк по 60 символов в каждой (один символ - одно действие, суммарно по 60 действий каждого ровера):

    U - движение на одну клетку вверх (уменьшить номер строки)
    L - движение на одну клетку влево (уменьшить номер столбца)
    D - движение на одну клетку вниз (увеличить номер строки)
    R - движение на одну клетку вправо (увеличить номер столбца)
    S - остаться на месте и ничего не делать
    T - остаться на месте и забрать самый старый заказ в текущей клетке
    P - остаться на месте и выдать заказ в текущей клетке

Роботы выполняют свои действия по очереди: сначала первое действие выполняет первый робот, затем второй и так далее до последнего робота. Потом первый робот выполняет второе действие, второй робот выполняет второе действие и так далее. В конце итерации каждый робот выполняет своё последнее действие и итерация заканчивается.

Несколько роботов могут занимать одну и ту же клетку. Робот не может перевозить более одного заказа одновременно.

Тестирующая система даст вашей программе прочитать свежие данные из входных данных только после того, как ваша программа вывела соответствующий запрос системе и выполнила операцию flush.
Пример
Ввод
Вывод

4 20 10  
....  
....  
....  
....  
7 7  
1  
1 1 4 4  
1  
1 4 4 1  
1  
4 4 1 1  
0  
4  
1 2 4 4  
2 2 3 3  
2 1 4 4  
2 2 4 4  
0  
0  

	

1  
4 4  
UUULLLTDDDRRRPSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
UUUTLLLDDDPSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
RRRTUUULLLPSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
RTDDDRRPUULLLTDDRRRPSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  
SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS  

Примечания

Вам предоставлены для ознакомления примеры тестовых данных, на которых будет тестироваться ваше решение. Гарантируется, что в системных тестах такие данные, как N, MaxTips, Costc, T и карта будут в точности такими же, как в ознакомительных тестах. Сами же заказы будут сгенерированы случайно, но тем же алгоритмом с тем же распределением, что и в ознакомительных тестах. Гарантируется, что значение D из системного теста будет отличаться от значения D в соответствующем ознакомительном тесте не более, чем на 1 процент.

Ознакомительные примеры доступны по ссылке: https://yadi.sk/d/gprf_snlEPb80A

