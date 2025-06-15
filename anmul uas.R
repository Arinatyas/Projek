---
  title: "anmul uas bismillah"
output: html_document
date: "2025-05-18"
---
  
  ```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## R Markdown

  
  ```{r cars}
# -----------------------------------------
# ANALISIS UAS - REGRESI LOGISTIK & LDA
# -----------------------------------------

# === LIBRARY ===
library(tidyverse)
library(caret)
library(e1071)
library(MASS)
library(caTools)
library(psych)
library(lmtest)
library(corrplot)
library(biotools)
library(ResourceSelection) 
library(car)               

# === LOAD DATA ===
data <- read.csv("Poblacion.csv", sep = ";", header = TRUE)
colnames(data) <- make.names(colnames(data))  

# Target sebagai faktor
data$target <- as.factor(data$student_dropout)

# === PREPROCESSING ===
# Ganti NA numerik dengan median
data[] <- lapply(data, function(x) {
  if (is.numeric(x)) {
    x[is.na(x)] <- median(x, na.rm = TRUE)
  }
  return(x)
})

# Cek struktur dan ringkasan
str(data)
summary(data)

# Statistik deskriptif numerik
describe(data[, sapply(data, is.numeric)])

# === KORELASI ===
num_cols <- sapply(data, is.numeric)
corr_matrix <- cor(data[, num_cols], use = "complete.obs")
corrplot(corr_matrix, method = "color", type = "upper", tl.cex = 0.6)

# === PEMILIHAN VARIABEL PREDIKTOR ===
# Ambil beberapa variabel numerik signifikan untuk model
selected_vars <- c("final_note", "semester_number", "total_credits", "math_exam", "verbal_exam", "payment_value")

# === SPLIT DATA ===
set.seed(123)
split <- sample.split(data$target, SplitRatio = 0.7)
train <- subset(data, split == TRUE)
test <- subset(data, split == FALSE)

# === REGRESI LOGISTIK ===
formula_log <- as.formula(paste("target ~", paste(selected_vars, collapse = " + ")))
log_model <- glm(formula_log, data = train, family = "binomial")
summary(log_model)

# === UJI ASUMSI REGRESI LOGISTIK ===

# 1. Multikolinearitas
vif(log_model)

# 2. Hosmer-Lemeshow Goodness-of-Fit Test
hoslem.test(as.numeric(train$target) - 1, fitted(log_model))

# === PREDIKSI ===
log_prob <- predict(log_model, newdata = test, type = "response")
log_class <- ifelse(log_prob > 0.5, 1, 0) %>% as.factor()
confusionMatrix(log_class, test$target)

# === LDA ===
lda_formula <- as.formula(paste("target ~", paste(selected_vars, collapse = " + ")))
lda_model <- lda(lda_formula, data = train)

# === UJI ASUMSI LDA ===

# 1. Multivariat Normalitas (Shapiro-Wilk tiap variabel di setiap kelas)
cat("Uji normalitas univariat (Shapiro-Wilk) per kelas:\n")
for (v in selected_vars) {
  by(train[[v]], train$target, function(x) {
    if (length(unique(x)) > 1) {
      sw <- shapiro.test(x)
      cat(paste0("Variabel: ", v, ", Group: ", unique(train$target)[1], " & ", unique(train$target)[2], " → p-value: ", round(sw$p.value, 4), "\n"))
    }
  })
}

# Multivariat normalitas bisa diuji dengan Mardia's test (paket MVN)
if (!require(MVN)) install.packages("MVN")
library(MVN)
cat("\nUji Mardia untuk multivariat normalitas:\n")
mvn_result <- mvn(data = train[, selected_vars], mvnTest = "mardia")
print(mvn_result$multivariateNormality)

# 2. Homogenitas Matriks Kovarians (Box's M test)
cat("\nUji Box's M untuk kesamaan matriks kovarians:\n")
boxm <- boxM(train[, selected_vars], train$target)
print(boxm)

# 3. Multikolinearitas antar variabel prediktor (korelasi tinggi)
cat("\nKorelasi antar variabel prediktor:\n")
corr_matrix_lda <- cor(train[, selected_vars])
print(round(corr_matrix_lda, 2))
corrplot(corr_matrix_lda, method = "number", type = "upper", tl.cex = 0.7)

lda_pred <- predict(lda_model, test)
confusionMatrix(lda_pred$class, test$target)

```
