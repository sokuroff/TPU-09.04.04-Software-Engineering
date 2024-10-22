# Получение данных
data("iris") # импорт датасета
str(iris) # вывод структуры датасета

summary(iris) # статистика всех переменных

# Разделение данных

set.seed(111) # установка зерна случайной 
# генерации для воспроизводимости

# scatter plots (матрица парных диаграмм) и корреляции
ind <- sample(2, nrow(iris), # делим датасет на две части по строкам
              replace = TRUE, # не уверен что это на что-то влияет
              prob = c(0.8, 0.2)) # делим части в отношении 80/20%
training <- iris[ind==1,] # 80% датасета в обучение
testing <- iris[ind==2,] # 20% в тест

library(psych) # подключаем библиотеку, которая содержит
               # функции для анализа данных

pairs.panels(training[,-5], # строим scatter plots для всех
                            # переменных в датасете
                            # кроме пятого столбца (species)
             gap = 0,       # промежуток между диаграммами равен 0
             bg = c("red", "yellow", "blue")[training$Species],
             # задаём разные цвета точек для каждого вида цветка
             # setosa - красный, versicolor - жёлтый, virginica синий
             pch=21) # стиль маркера: круглый, с заливкой фона

pc <- prcomp(training[,-5], # берём все независимые признаки
             center = TRUE, # центрируем данные
             scale. = TRUE) # масштабируем признаки
attributes(pc) # получаем атрибуты 

library(devtools)
library(ggbiplot)

data <- read.csv("train.csv")
data <- data[ , -ncol(data)]
data <- na.omit(data)
summary(data)

data$Gender <- as.numeric(factor(data$Gender))
data$Ever_Married <- as.numeric(factor(data$Ever_Married))
data$Graduated <- as.numeric(factor(data$Graduated))
data$Profession <- as.numeric(factor(data$Profession))
data$Spending_Score <- as.numeric(factor(data$Spending_Score))
data$Var_1 <- as.numeric(factor(data$Var_1))

ind <- sample(2, nrow(data), # делим датасет на две части по строкам
              replace = TRUE, # не уверен что это на что-то влияет
              prob = c(0.8, 0.2)) # делим части в отношении 80/20%
training <- data[ind==1,] # 80% датасета в обучение
testing <- data[ind==2,] # 20% в тест

library(psych) # подключаем библиотеку, которая содержит
# функции для анализа данных

pairs.panels(training[,-10], # строим scatter plots для всех
             # переменных в датасете
             # кроме пятого столбца (species)
             gap = 0,       # промежуток между диаграммами равен 0
             bg = c("red", "yellow", "blue")[training$Species],
             # задаём разные цвета точек для каждого вида цветка
             # setosa - красный, versicolor - жёлтый, virginica - синий
             pch=21) # стиль маркера: круглый, с заливкой фона

pc <- prcomp(training[,-10], # берём все независимые признаки
             center = TRUE, # центрируем данные
             scale. = TRUE) # масштабируем признаки
attributes(pc) # получаем атрибуты 

print(pc)

summary(pc)

library(devtools)
library(ggbiplot)

training$Var_1 <- as.factor(training$Var_1)

g <- ggbiplot(pc, # создаём график, передаём туда PC
              obs.scale = 1, # размер наблюдений равен 1
              var.scale = 1, # размер переменных равен 1
              groups = training$Var_1, # точки на графике будут раскрашены в зависимости от группы (вида цветка)
              ellipse = TRUE, # доверительные эллипсы 
              circle = TRUE, # добавляет окружность радиусом 1 для точек
              ellipse.prob = 0.68) # уровень вероятности для эллипсов
g <- g + scale_color_discrete(name = '') # настройка цветовой шкалы без легенды
g <- g + theme(legend.direction = 'horizontal',
               legend.position = 'top') # корректировка отображения легенды
print(g)

trg <- predict(pc, training) # преобразование обучающих данных с помощью PCA
trg <- data.frame(trg, training[10]) # формируем дата-фрейм с ответами (5й столбец)
tst <- predict(pc, testing) # преобразование также тестовой выборки
tst <- data.frame(tst, testing[10]) # формируем дата-фрейм с ответами (5й столбец)

trg$Var_1 <- as.factor(trg$Var_1)
mymodel <- multinom(Var_1 ~ ., data = as.data.frame(cbind(trg$Var_1, pc$x)))
summary(mymodel)


library(nnet)


trg$Species <- relevel(trg$Species, ref = "setosa")
mymodel <- multinom(Species~PC1+PC2, data = trg)
summary(mymodel)