setwd("~/R_data_analyze/ML/DNA")
library(dplyr)
library(tidyr)
library(ggplot2)
library(psych)
library(umap)
library(plotly)
library(e1071)

DNAsample <- read.csv("splicesites.csv")
DNAsample$X <- NULL
build_umap <- function(DNAsample) {
  DNAfeatures <- select(DNAsample, !Class)
  DNAfeatures$X <- NULL
  # at first step let's don't see difference between ei and ie
  DNAsample$simple_class <- as.factor(ifelse(DNAsample$Class == "n",
                                             0, 1))
  ifelse(DNAsample == "n", 0, 1)
  y <- rep(colnames(DNAfeatures), ncol(DNAfeatures))
  x <- sort(y)
  phi_table <- data.frame(x, y)
  
  # build covariation matrix
  phi_table$value <- data.frame(x, y) %>%
    apply(MARGIN = 1, function(param) phi(table(DNAfeatures[param])))
  
  phi_matrix <- spread(phi_table, x, value)
  
  rownames(phi_matrix) <- phi_matrix$y
  phi_matrix <- as.matrix(select(phi_matrix, !y))
  
  # build svd of cov.matrix and transform binary variables
  phi_svd <- svd(phi_matrix)
  
  #build umap
  
  scored_sites <- as.matrix((DNAfeatures %>%
                               mutate_all(as.numeric) - 1)) %*%
    phi_svd$v %>% Rtsne::normalize_input()
  
  umap_of_sites <- umap(scored_sites)
  umap_of_sites$layout <- as.data.frame(umap_of_sites$layout)
  umap_of_sites$layout$class <- DNAsample$simple_class
  umap_of_sites$layout$index <- 1:nrow(DNAsample)
  umap_of_sites$layout$hcls <- as.factor(cutree(hclust(dist(umap_of_sites$layout[c("V1","V2")])),
                                                k = 3))
  
  umap_of_sites$phi_matrix <- phi_matrix
  umap_of_sites$phi_svd <- phi_svd
  umap_of_sites$pca_scored_sites <- scored_sites
    
  return(umap_of_sites)
}

totall_umap <- build_umap(DNAsample)


totall_umap$layout %>% ggplot(aes(x = V1, y = V2, color = class)) +
  geom_point(size = 0.7, alpha = 0.5) + xlab("UMAP1") + ylab("UMAP2") +
  ggtitle("Totall")

# remove outliers
# radius should to be positive 
truncate <- function(X, Y, radius) {
  norms <- sqrt((X ^ 2) + (Y ^ 2))
  # norms have only positive values
  # let's estimate probability get such or greater values and if prob is less return FALSE
  return(sapply(norms, function(x) ifelse(x <= abs(radius), T, F)))  
  
  }
  

totall_umap$layout <- totall_umap$layout[truncate(totall_umap$layout$V1,
                                                  totall_umap$layout$V2, radius = 20),]



totall_umap$layout %>% ggplot(aes(x = V1, y = V2, color = class)) +
  geom_point(size = 0.7, alpha = 0.5) + xlab("UMAP1") + ylab("UMAP2") +
  ggtitle("Without outliers")

splitting <- sample(c(T,F),
       nrow(totall_umap$layout),
       replace = T)

sample1umap <- totall_umap$layout[splitting,]

sample1umap %>% ggplot(aes(x = V1, y = V2, color = class)) +
  geom_point(size = 0.7, alpha = 0.5) + xlab("UMAP1") + ylab("UMAP2") +
  ggtitle("sample1umap")


sample2umap <- totall_umap$layout[!splitting,]

sample2umap %>% ggplot(aes(x = V1, y = V2, color = class)) +
  geom_point(size = 0.7, alpha = 0.5) + xlab("UMAP1") + ylab("UMAP2") +
  ggtitle("sample2umap")

# size of classes
table(sample1umap$class)
table(sample2umap$class)


build_svm <- function(train, test, kernel) {

  res <- list()
  classificator <- svm(x = train[c("V1","V2")],
                     y = train$class,
                     type = "C-classification",
                     kernel = kernel,
                     probability = TRUE)

  result_prediction <- predict(classificator, type = "response",
                               newdata = test[c("V1","V2")],
              decision.values = T, probability = TRUE)
  
  res$classificator <- classificator
  res$prediction <- result_prediction
  return(res)

}
# compare different kernels

polynomial1vs2 <- build_svm(sample1umap, sample2umap, "polynomial")
polynomial2vs1 <- build_svm(sample2umap, sample1umap, "polynomial")

sigmoid1vs2 <- build_svm(sample1umap, sample2umap, "sigmoid")
sigmoid2vs1 <- build_svm(sample2umap, sample1umap, "sigmoid")

radial1vs2 <- build_svm(sample1umap, sample2umap, "radial")
radial2vs1 <- build_svm(sample2umap, sample1umap, "radial")


# Evaluate phrobenius norm in cross-prediction
phrobenius_norm <- function(pred, rev_pred, actual, rev_actual) {
  res <- list()
  forward <- as.matrix(table(pred,
                             actual))
  reverse <- as.matrix(table(rev_pred,
                             rev_actual))
  res$forward <- forward
  res$reverse <- reverse
  res$metrics <- list()
  res$metrics$accuracy_forward <- sum(diag(forward)) / sum(forward) 
  res$metrics$recall_forward <- forward[1,1] / (forward[1,1] + forward[2,1])
  res$metrics$precision_forward <- forward[1,1] / (forward[1,1] + forward[1,2])
  res$metrics$f_mesuare_forward <- 2 * res$metrics$precision_forward *
    res$metrics$recall_forward / (res$metrics$precision_forward +
                                    res$metrics$recall_forward)
  
  res$metrics$accuracy_reverse <- sum(diag(reverse)) / sum(reverse)
  res$metrics$recall_reverse <- reverse[1,1] / (reverse[1,1] + reverse[2,1])
  res$metrics$precision_reverse <- reverse[1,1] / (reverse[1,1] + reverse[1,2])
  res$metrics$f_mesuare_reverse <- 2 * res$metrics$precision_reverse *
    res$metrics$recall_reverse / (res$metrics$precision_reverse +
                                    res$metrics$recall_reverse)
  
  return(res)
  
}


draw_ROC <- function(probs_pred, actual) {
  
  prediction(probs_pred,
             actual) %>%
    performance("tpr","fpr") %>%
    plot(colorize=TRUE)
  
}

polynomial <- phrobenius_norm(polynomial1vs2$prediction,
                polynomial2vs1$prediction,
                sample2umap$class,
                sample1umap$class)

draw_ROC(attr(polynomial1vs2$prediction, "probabilities")[,"1"], sample2umap$class)
title("Polynomial (forward)")

round(AUC::auc(AUC::roc(attr(polynomial1vs2$prediction,
                             "probabilities")[,"1"],
                        sample2umap$class)), 3)

draw_ROC(attr(polynomial2vs1$prediction, "probabilities")[,"1"], sample1umap$class)
title("Polynomial (reverse)")

round(AUC::auc(AUC::roc(attr(polynomial2vs1$prediction,
                             "probabilities")[,"1"],
                        sample1umap$class)), 3)



radial <- phrobenius_norm(radial1vs2$prediction,
                          radial2vs1$prediction,
                              sample2umap$class,
                              sample1umap$class)

draw_ROC(attr(radial1vs2$prediction, "probabilities")[,"1"], sample2umap$class)
title("Radial (forward)")

round(AUC::auc(AUC::roc(attr(radial1vs2$prediction,
                             "probabilities")[,"1"],
                        sample2umap$class)), 3)

draw_ROC(attr(radial2vs1$prediction, "probabilities")[,"1"], sample1umap$class)
title("Radial (reverse)")

round(AUC::auc(AUC::roc(attr(radial2vs1$prediction,
                             "probabilities")[,"1"],
                        sample1umap$class)), 3)


sigmoid <- phrobenius_norm(sigmoid1vs2$prediction,
                           sigmoid2vs1$prediction,
                          sample2umap$class,
                          sample1umap$class)


draw_ROC(attr(sigmoid1vs2$prediction, "probabilities")[,"1"], sample2umap$class)
title("Sigmoid (forward)")

round(AUC::auc(AUC::roc(attr(sigmoid1vs2$prediction,
                             "probabilities")[,"1"],
                        sample2umap$class)), 3)

draw_ROC(attr(sigmoid2vs1$prediction, "probabilities")[,"1"], sample1umap$class)
title("Sigmoid (reverse)")

round(AUC::auc(AUC::roc(attr(sigmoid2vs1$prediction,
                             "probabilities")[,"1"],
                        sample1umap$class)), 3)


