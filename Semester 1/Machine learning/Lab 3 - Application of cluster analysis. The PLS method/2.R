data <- read.csv("winequality-red.csv", sep = ";", header = TRUE, quote = "\"")
data$quality <- as.factor(data$quality)


library(mixOmics) # подключаем его
set.seed(5249) # для воспроизводимости результатов

X <- data[, -ncol(data)]
Y <- data$quality

dim(X) # проверяем размерность датафрейма X
summary(Y) # проверяем распределение классов

# Применяем метод главных компонент, 10 компонент, центрируем и нормируем
pca.wine = pca(X, ncomp = 10, center = TRUE, scale = TRUE) 
plot(pca.wine)  # столбчатый график собственных значений

plotIndiv(pca.wine, group = data$quality, ind.names = FALSE,  
          legend = TRUE, title = 'PCA on wine, comp 1 - 2') 

wine.splsda <- splsda(X, Y, ncomp = 10)  # устанавливаем ncomp равным 10 для сравнения с PCA в дальнейшем

plotIndiv(wine.splsda , 
          group = data$quality, ind.names = FALSE,  
          ellipse = TRUE, # доверительный эллипс 0.95
          legend = TRUE, title = 'PLSDA с доверительными эллипсами')

# использование max.dist для измерения чтобы сформировать границы классов
background = background.predict(wine.splsda, comp.predicted=2, dist = "max.dist")

# график классов проецированных на первые две компоненты sPLS-DA
plotIndiv(wine.splsda,
          group = data$quality, ind.names = FALSE,
          background = background, 
          legend = TRUE, title = "PLSDA с границами классов")

# оцениваем производительность модели 
perf.splsda.wine <- perf(wine.splsda, validation = "Mfold", # кросс-валидация типа MFold
                          folds = 10, nrepeat = 10, # 5 частей, 10 повторений
                          progressBar = FALSE, auc = TRUE) # подключаем площадь под кривой (AUC)

# визуализация результатов оценки
plot(perf.splsda.wine, col = color.mixo(5:7), sd = TRUE,
     legend.position = "horizontal")

perf.splsda.wine$choice.ncomp # наилучшее значение количества компонент по мнению perf()

# cоздание списка значений keepX для тестирования
list.keepX <- c(1:10,  seq(20, 300, 10))

tune.splsda.wine <- tune.splsda(X, Y, ncomp = 6, # 6 компоненты
                                 validation = 'Mfold',
                                 folds = 10, nrepeat = 10, 
                                 dist = 'max.dist', # метрика max.dist
                                 measure = "BER", # используем сбалансированную частоту ошибок
                                 test.keepX = list.keepX,
                                 cpus = 2) # разрешение на распар

plot(tune.splsda.wine, col = color.jet(6)) # Вывод на график

tune.splsda.wine$choice.ncomp$ncomp # оптимальное количество компонент согласно tune.splsda()

tune.splsda.wine$choice.keepX # оптимальное количество переменных согласно tune.splsda()

optimal.ncomp <- tune.splsda.wine$choice.ncomp$ncomp
optimal.keepX <- tune.splsda.wine$choice.keepX[1:optimal.ncomp]

final.splsda <- splsda(X, Y, 
                       ncomp = optimal.ncomp, 
                       keepX = optimal.keepX)

plotIndiv(final.splsda, comp = c(1,2), # графики, полученные с помощью финальной модели
          group = data$quality, ind.names = FALSE, # цвета по классам
          ellipse = TRUE, legend = TRUE, # доверительные эллипсы 0.95
          title = ' (a) sPLS-DA на SRBCT, компоненты 1 & 2')

# задаём легенду
legend=list(legend = levels(Y), # set of classes
            col = unique(color.mixo(Y)), # set of colours
            title = "Tumour Type", # legend title
            cex = 0.7) # legend size

# создаём CIM
cim <- cim(final.splsda, row.sideColors = color.mixo(Y), 
           legend = legend)

# формируем новый perf() с использованием финальной настроенной модели
perf.splsda.wine <- perf(final.splsda, 
                          folds = 10, nrepeat = 10, # кросс-валидация
                          validation = "Mfold", dist = "max.dist",  # метрика max.dist 
                          progressBar = FALSE)

# выводим на график стабильность каждого признака для первых трёх компонент, 'h' означает гистограмму
par(mfrow=c(3,2))
plot(perf.splsda.wine$features$stable[[1]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features', 
     main = '(a) Comp 1', las =2)
plot(perf.splsda.wine$features$stable[[2]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features', 
     main = '(b) Comp 2', las =2)
plot(perf.splsda.wine$features$stable[[3]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features',
     main = '(c) Comp 3', las =2)
plot(perf.splsda.wine$features$stable[[4]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features',
     main = '(d) Comp 4', las =2)
plot(perf.splsda.wine$features$stable[[5]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features',
     main = '(e) Comp 5', las =2)
plot(perf.splsda.wine$features$stable[[6]], type = 'h', 
     ylab = 'Stability', 
     xlab = 'Features',
     main = '(f) Comp 6', las =2)

var.name.short <- substr(names(X), 1, 10)

plotVar(final.splsda, comp = c(1,6), var.names = list(var.name.short), cex = 3) # генерируем корреляционный круг


# Разделение датасета на обучающую и тестовую выборки в соотношении 80/20
ind <- sample(2, nrow(data), replace = TRUE, prob = c(0.8, 0.2))

# Отдельно формируем X и Y для обучающей и тестовой выборок
X.train <- data[ind == 1, -ncol(data)]  # Признаки для обучения (80%)
Y.train <- data[ind == 1, ncol(data)]   # Целевая переменная для обучения (80%)

X.test <- data[ind == 2, -ncol(data)]   # Признаки для тестирования (20%)
Y.test <- data[ind == 2, ncol(data)]    # Целевая переменная для тестирования (20%)

# обучение модели
train.splsda.wine <- splsda(X.train, Y.train, ncomp = optimal.ncomp, keepX = optimal.keepX)

# используем модель на сете X test
predict.splsda.wine <- predict(train.splsda.wine, X.test, 
                                dist = "mahalanobis.dist")

# Извлечение предсказаний для второй компоненты
predict.comp2 <- predict.splsda.wine$class$mahalanobis.dist[, 2]

table(factor(predict.comp2, levels = levels(Y)), Y.test)


# оценка предсказательной способности для 6 компонент
predict.comp6 <- predict.splsda.wine$class$mahalanobis.dist[,6]
table(factor(predict.comp6, levels = levels(Y)), Y.test)


auc.splsda = auroc(final.splsda, roc.comp = 1, print = FALSE) # AUROC для первой компоненты

auc.splsda = auroc(final.splsda, roc.comp = 6, print = FALSE) # AUROC для всех компонент
