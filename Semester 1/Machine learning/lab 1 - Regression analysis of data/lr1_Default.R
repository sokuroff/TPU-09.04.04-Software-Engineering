set.seed(500) # установка seed для определения рандома
library(MASS) # подключение библиотеки с датасетами
data <- Boston # перекладка датасеа Boston в переменную data

apply(data,2,function(x) sum(is.na(x))) # проверка целостности данных

index <- sample(1:nrow(data),round(0.75*nrow(data))) # забираем 75% случайных индексов записей
train <- data[index,] # 75% всех индексов идут на обучение
test <- data[-index,] # оставшаяся часть (25%) на тест

#LM - linear model
lm.fit <- glm(medv~., data=train) # собираем модель линейной регрессии и обучаем её на train сете
summary(lm.fit) # отчёт о модели
pr.lm <- predict(lm.fit, test) # кладём в переменную предсказываемые lm значения medv 
MSE.lm <- sum((pr.lm - test$medv)^2)/nrow(test) # считаем MSE

#Preparing to fit the neural network

maxs <- apply(data, 2, max) # получаем максимальные значения каждого признака
mins <- apply(data, 2, min) # получаем минимальные значения каждого признака

scaled <- as.data.frame(scale(data, center = mins, scale = maxs - mins)) # масштабируем данные в диапазон [0, 1]

train_ <- scaled[index,] # 75% в train
test_ <- scaled[-index,] # 25% в test

library(neuralnet) # подключение библиотеки с нейросетями
n <- names(train_) # n - имена всех столбцов датасета
f <- as.formula(paste("medv ~", paste(n[!n %in% "medv"], collapse = " + "))) # генерация формулы из string
nn <- neuralnet(f,data=train_,hidden=c(5,3),linear.output=T) # создаём MLP и обучаем его на train 

plot(nn) # вывод MLP

#Predicting medv using the neural network

pr.nn <- compute(nn,test_[,1:13]) # прогноз нейросети на тестовой выборке на первых 13 столбцах (без medv)
pr.nn_ <- pr.nn$net.result*(max(data$medv)-min(data$medv))+min(data$medv) # возвращаем нормализованные [0, 1] предсказания обратно [min, max]
test.r <- (test_$medv)*(max(data$medv)-min(data$medv))+min(data$medv) # то же самое, что и в прошлой строчке, только для medv
MSE.nn <- sum((test.r - pr.nn_)^2)/nrow(test_) # считаем MSE

print(paste(MSE.lm,MSE.nn)) # выводим MSE LM и MSE NN

par(mfrow=c(1,2)) # создаём в одном окне 2 графика

# Построение графиков, которые позволяют изуализировать, 
# насколько близки прогнозы моделей к фактическим значениям.
plot(test$medv,pr.nn_,col='red',main='Real vs predicted NN',pch=18,cex=0.7)
abline(0,1,lwd=2)
legend('bottomright',legend='NN',pch=18,col='red', bty='n')

plot(test$medv,pr.lm,col='blue',main='Real vs predicted lm',pch=18, cex=0.7)
abline(0,1,lwd=2)
legend('bottomright',legend='LM',pch=18,col='blue', bty='n', cex=.95)

#A (fast) cross validation

library(boot) # загружаем библиотеку для кросс-валидации
set.seed(200) # устанавливаем зерно случайных чисел
lm.fit <- glm(medv~.,data=data) # вновь создаём модель линейной регрессии
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
  
  nn <- neuralnet(f,data=train.cv,hidden=c(5,2),linear.output=T) # обучаем нейр. сеть
  
  pr.nn <- compute(nn,test.cv[,1:13]) # вычисляем прогнозы на тестовых данных
  pr.nn <- pr.nn$net.result*(max(data$medv)-min(data$medv))+min(data$medv) # обратная нормализация
  
  test.cv.r <- (test.cv$medv)*(max(data$medv)-min(data$medv))+min(data$medv) # обратная нормализация
  
  cv.error[i] <- sum((test.cv.r - pr.nn)^2)/nrow(test.cv) # сохраняем MSE текущего фолда
  
  pbar$step() # шаг для прогресс-бара
}
mean(cv.error) # считаем среднюю ошибку кросс-валидаци
cv.error # вывод полного вектора ошибок (ошибки каждого фолда)

boxplot(cv.error,xlab='MSE CV',col='cyan',
        border='blue',names='CV error (MSE)',
        main='CV error (MSE) for NN',horizontal=TRUE)


