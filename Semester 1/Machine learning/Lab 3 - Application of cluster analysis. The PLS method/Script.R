
library(mixOmics) # подключаем его
set.seed(5249) # для воспроизводимости результатов

data(srbct) # Получаем данные small round bull cell tumour
X <- srbct$gene # используем уровни экспрессии генов как матрицу X
Y <- srbct$class # используем классы как матрицу Yт

dim(X) # проверяем размерность датафрейма X

summary(Y) # проверяем распределение классов


# Применяем метод главных компонент, 10 компонент, центрируем и нормируем
pca.srbct = pca(X, ncomp = 10, center = TRUE, scale = TRUE) 
plot(pca.srbct)  # столбчатый гарфик собственных значений

plotIndiv(pca.srbct, group = srbct$class, ind.names = FALSE,  
          legend = TRUE, title = 'PCA on SRBCT, comp 1 - 2') 

srbct.splsda <- splsda(X, Y, ncomp = 10)  # устанавливаем ncomp равным 10 для сравнения с PCA в дальнейшем

# оцениваем производительность модели 
perf.splsda.srbct <- perf(srbct.splsda, validation = "Mfold", # кросс-валидация типа MFold
                          folds = 5, nrepeat = 10, # 5 частей, 10 повторений
                          progressBar = FALSE, auc = TRUE) # подключаем площадь под кривой (AUC)

# визуализация результатов оценки
plot(perf.splsda.srbct, col = color.mixo(5:7), sd = TRUE,
     legend.position = "horizontal")
