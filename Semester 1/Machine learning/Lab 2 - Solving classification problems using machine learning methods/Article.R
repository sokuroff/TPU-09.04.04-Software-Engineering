data("iris") # импорт датасета
str(iris) # вывод структуры датасета

summary(iris) # статистика всех переменных

# Разделение данных

set.seed(111) # установка зерна случайной 
# генерации для воспроизводимости

#
ind <- sample(2, nrow(iris),
              replace = TRUE,
              prob = c(0.8, 0.2))
training <- iris[ind==1,]
testing <- iris[ind==2,]
