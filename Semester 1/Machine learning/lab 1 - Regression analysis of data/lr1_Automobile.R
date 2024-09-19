data <- read.csv("Automobile.csv")

data <- data[, -c(1, ncol(data))] # удаляем ненужные стобцы типа названия автомобиля
library(tidyverse)
data <- drop_na(data) # удаляем NA из датасета

apply(data,2,function(x) sum(is.na(x))) # проверка целостности данных

index <- sample(1:nrow(data),round(0.75*nrow(data))) # забираем 75% случайных индексов записей
train <- data[index,] # 75% всех индексов идут на обучение
test <- data[-index,] # оставшаяся часть (25%) на тест

#LM - linear model
lm.fit <- glm(acceleration~., data=train) # собираем модель линейной регрессии и обучаем её на train сете
summary(lm.fit) # отчёт о модели
pr.lm <- predict(lm.fit, test) # кладём в переменную предсказываемые lm значения acceleration 
MSE.lm <- sum((pr.lm - test$acceleration)^2)/nrow(test) # считаем MSE

#Preparing to fit the neural network

maxs <- apply(data, 2, max) # получаем максимальные значения каждого признака
mins <- apply(data, 2, min) # получаем минимальные значения каждого признака

scaled <- as.data.frame(scale(data, center = mins, scale = maxs - mins)) # масштабируем данные в диапазон [0, 1]

train_ <- scaled[index,] # 75% в train
test_ <- scaled[-index,] # 25% в test

library(neuralnet) # подключение библиотеки с нейросетями
n <- names(train_) # n - имена всех столбцов датасета
f <- as.formula(paste("acceleration ~", paste(n[!n %in% "acceleration"], collapse = " + "))) # генерация формулы из string
nn <- neuralnet(f,data=train_,hidden=c(5,3),linear.output=T) # создаём MLP и обучаем его на train 

plot(nn) # вывод MLP

#Predicting wine acceleration using the neural network

# Подготовка тестовых данных (удаление столбца 'acceleration')
test_data <- test_[, -which(names(test_) == "acceleration")]

pr.nn <- neuralnet::compute(nn, test_data)
pr.nn_ <- pr.nn$net.result*(max(data$acceleration)-min(data$acceleration))+min(data$acceleration) # возвращаем нормализованные [0, 1] предсказания обратно [min, max]
test.r <- (test_$acceleration)*(max(data$acceleration)-min(data$acceleration))+min(data$acceleration) # то же самое, что и в прошлой строчке, только для quality
MSE.nn <- sum((test.r - pr.nn_)^2)/nrow(test_) # считаем MSE

print(paste(MSE.lm,MSE.nn)) # выводим MSE LM и MSE NN

par(mfrow = c(1, 2)) # создаём в одном окне 2 графика
# Построение графиков, которые позволяют изуализировать, 
# насколько близки прогнозы моделей к фактическим значениям.
plot(test$acceleration,pr.nn_,col='red',main='Real vs predicted NN',pch=18,cex=0.7)
abline(0,1,lwd=2)
legend('bottomright',legend='NN',pch=18,col='red', bty='n')

plot(test$acceleration,pr.lm,col='blue',main='Real vs predicted lm',pch=18, cex=0.7)
abline(0,1,lwd=2)
legend('bottomright',legend='LM',pch=18,col='blue', bty='n', cex=.95)

library(boot) # загружаем библиотеку для кросс-валидации
set.seed(200) # устанавливаем зерно случайных чисел
lm.fit <- glm(acceleration~.,data=data) # вновь создаём модель линейной регрессии
cv.glm(data,lm.fit,K=10)$delta[1] # выполняем кросс-валидацию на 10 фолдах

set.seed(450) # меняем зерно случайных чисел
cv.error <- NULL # создаём переменную для хранения ошибки кросс-валидации
k <- 10 # количество фолдов

library(plyr) # библиотека для отображения прогресс-баров
pbar <- create_progress_bar('text') # выбираем текстовый прогресс бар
pbar$init(k) # инициализируем его с максимальным количеством шагов равным k


for(i in 1:k){ # цикл с 1 до k
  index <- sample(1:nrow(data),round(0.9*nrow(data))) # делим выборку 90/10%
  train.cv <- scaled[index,] # 90%
  test.cv <- scaled[-index,] # 10%
  
  test_data <- test.cv[, -which(names(test_) == "acceleration")]
  nn <- neuralnet(f,data=train.cv,hidden=c(5,2),linear.output=T) # обучаем нейр. сеть
  pr.nn <- neuralnet::compute(nn,test_data) # вычисляем прогнозы на тестовых данных
  pr.nn <- pr.nn$net.result*(max(data$acceleration)-min(data$acceleration))+min(data$acceleration) # обратная нормализация
  
  test.cv.r <- (test.cv$acceleration)*(max(data$acceleration)-min(data$acceleration))+min(data$acceleration) # обратная нормализация
  
  cv.error[i] <- sum((test.cv.r - pr.nn)^2)/nrow(test.cv) # сохраняем MSE текущего фолда
  
  pbar$step() # шаг для прогресс-бара
}
mean(cv.error) # считаем среднюю ошибку кросс-валидаци
cv.error # вывод полного вектора ошибок (ошибки каждого фолда)

boxplot(cv.error,xlab='MSE CV',col='cyan',
        border='blue',names='CV error (MSE)',
        main='CV error (MSE) for NN',horizontal=TRUE)


