setwd("~/R_data_analyze/ML/DNA")
library(dplyr)
library(tidyr)
library(ggplot2)
library(psych)
library(umap)
library(plotly)
library(mlbench)
data(DNA)

DNAfeatures <- select(DNA, !Class)

y <- rep(colnames(DNAfeatures), ncol(DNAfeatures))
x <- sort(y)
phi_table <- data.frame(x, y)
# build covariation matrix
phi_table$value <- data.frame(x, y) %>%
  apply(MARGIN = 1, function(param) phi(table(DNAfeatures[param])))

ggplot(phi_table, aes(x = x, y = y, fill = value)) + geom_tile()
# look at cor coefs
hist(phi_table$value)

phi_matrix <- spread(phi_table, x, value)

rownames(phi_matrix) <- phi_matrix$y
phi_matrix <- as.matrix(select(phi_matrix, !y))
heatmap(phi_matrix)

# build svd of cov.matrix and transform binary variables
phi_svd <- svd(phi_matrix)

# percent of variance for each component is very small
data.frame(components = 1:length(phi_svd$d),
           variance = 100 * phi_svd$d / sum(phi_svd$d)) %>%
  ggplot(aes(x = components, y = variance)) + geom_point() + geom_line()

# build umap
scored_sites <- as.matrix((DNAfeatures %>%
                             mutate_all(as.numeric) - 1)) %*%
                            phi_svd$v %>% Rtsne::normalize_input()

umap_of_sites <- umap(scored_sites[,1:120])

umap_of_sites$layout <- as.data.frame(umap_of_sites$layout)
umap_of_sites$layout$class <- DNA$Class
umap_of_sites$layout$index <- 1:nrow(DNA)
umap_of_sites$layout$hcls <- as.factor(cutree(hclust(dist(umap_of_sites$layout[c("V1","V2")])), k = 3))

# On plot some outliers observed
umap_of_sites$layout %>% ggplot(aes(x = V1, y = V2)) + geom_point(data = filter(umap_of_sites$layout, hcls == 1),
                                                                                size = 0.7, alpha = 0.5)

umap_of_sites$filt_layout <- filter(umap_of_sites$layout, V2 > -10 & V1 < 2 & hcls == 1)


umap_of_sites$filt_layout %>%
  ggplot(aes(x = V1, y = V2, color = class)) +
  geom_point(size = 0.7, alpha = 0.5)

# take data without outliers
filt_DNA <- DNA[umap_of_sites$filt_layout$index,]
write.csv(filt_DNA, file="splicesites.csv")

# make sampling for further cross-validation
DNAsample1 <- filt_DNA[!sample(c(T,F), 3164, replace = T),]
DNAsample2 <- filt_DNA[sample(c(T,F), 3164, replace = T),]
write.csv(DNAsample1, file="DNAsample1.csv")
write.csv(DNAsample2, file="DNAsample2.csv")


# Build svm and check perfomance of our model
# 1) train: DNAsample1, test: DNAsample2 
# 2) train: DNAsample2, test: DNAsample1
# build two svm`s and compare metrics. 

