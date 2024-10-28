if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager") # устанавливаем менеджер пакетов
BiocManager::install("mixOmics") # устанавливаем mixOmics

library(mixOmics) # подключаем его
set.seed(5249) # для воспроизводимости результатов

data(srbct) # Получаем данные small round bull cell tumour
X <- srbct$gene # используем уровни экспрессии генов как матрицу X
Y <- srbct$class # используем классы как матрицу Y

dim(X) # проверяем размерность датафрейма X

summary(Y) # проверяем распределение классов


# Применяем метод главных компонент, 10 компонент, центрируем и нормируем
pca.srbct = pca(X, ncomp = 10, center = TRUE, scale = TRUE) 
plot(pca.srbct)  # столбчатый гарфик собственных значений

plotIndiv(pca.srbct, group = srbct$class, ind.names = FALSE,  
          legend = TRUE, title = 'PCA on SRBCT, comp 1 - 2') 