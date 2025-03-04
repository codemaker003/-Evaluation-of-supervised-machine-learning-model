import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error,r2_score
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve
from sklearn.tree import plot_tree
from sklearn.preprocessing import OneHotEncoder
import numpy as np


def main():
    # Main content
    st.title('Evaluation of supervised machine learning model')
    st.write('### Upload Dataset')

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        # Load the dataset
        df = pd.read_csv(uploaded_file)
        st.write('### Dataset')
        st.write(df.head())

    # Checkbox to trigger replacing null values and concatenating data
        st.sidebar.title("Data Preprocessing")
        preprocess_checkbox = st.sidebar.checkbox("Replace Null Values and Concatenate")
        if preprocess_checkbox:
    # Fill null values with next valid observation
            df.fillna(method='bfill', inplace=True)
            st.write('### Null Values Replaced')
            st.write(df.head())

    # Perform one-hot encoding
            df = pd.get_dummies(df)
            st.write('### Encoded Data')
            st.write(df.head())



        # Data Analytics Section
        st.sidebar.title("Data Analysis")
        selected_features = st.sidebar.multiselect("Select Features", df.columns)
        if selected_features:
            st.write("### Data Analysis")
            # Distribution plots
            for feature in selected_features:
                if df[feature].dtype == 'int64' or df[feature].dtype == 'float64':
                    st.write(f"#### {feature} Distribution")
                    plt.figure(figsize=(8, 5))
                    sns.histplot(df[feature], kde=True)
                    plt.xlabel(feature)
                    plt.ylabel("Frequency")
                    st.pyplot()

            # Boxplot for numerical features
            st.write("#### Boxplot for Numerical Features")
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df[selected_features])
            plt.xticks(rotation=45)
            st.pyplot()

            # Correlation Heatmap
            st.write("#### Correlation Heatmap")
            corr = df[selected_features].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm')
            st.pyplot()

            # Pairplot
            st.write("#### Pairplot")
            sns.pairplot(df[selected_features])
            st.pyplot()

            # Countplots for categorical features
            categorical_features = [feature for feature in selected_features if df[feature].dtype == 'object']
            for feature in categorical_features:
                st.write(f"#### {feature} Countplot")
                plt.figure(figsize=(8, 5))
                sns.countplot(data=df, x=feature)
                plt.xticks(rotation=45)
                st.pyplot()

       

        C = 1.0  # Default value for C
        # Sidebar - Model Selection and Hyperparameter Tuning
        st.sidebar.title('Model Configuration')
        model_name = st.sidebar.selectbox('Select Model', ['Random Forest', 'Logistic Regression', 'SVM', 'K-Nearest Neighbors', 'Decision Tree', 'Linear Regression'])
        if model_name == 'Random Forest':
            n_estimators = st.sidebar.slider('Number of Estimators', 1, 100, 10)
            max_depth = st.sidebar.slider('Max Depth', 1, 20, 10)
        elif model_name == 'SVM':
            C = st.sidebar.slider('Regularization Parameter (C)', 0.01, 10.0, 1.0)
            kernel = st.sidebar.selectbox('Kernel', ['linear', 'poly', 'rbf', 'sigmoid'])
        elif model_name == 'K-Nearest Neighbors':
            n_neighbors = st.sidebar.slider('Number of Neighbors', 1, 20, 5)
        elif model_name == 'Decision Tree':
            max_depth = st.sidebar.slider('Max Depth', 1, 20, 10)
        elif model_name == 'Gradient Boosting':
            n_estimators_gb = st.sidebar.slider('Number of Estimators', 1, 100, 10)
            learning_rate_gb = st.sidebar.slider('Learning Rate', 0.01, 1.0, 0.1)

        # Select features (X values)
        target_column = st.sidebar.selectbox('Select Target Variable (y)', df.columns)

         # Select target variable (y)
        
        selected_features = st.sidebar.multiselect("Select Features (X)", [col for col in df.columns if col != target_column])
   

        # Train and evaluate the selected model
        train_button = st.sidebar.button("Evaluate the model and Output plots")
        if train_button:
            X = df[selected_features]
            y = df[target_column]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            if model_name == 'Random Forest':
                st.write('### Random Forest Configuration')
                st.write(f'Number of Estimators: {n_estimators}')
                st.write(f'Max Depth: {max_depth}')

                # Train the model
                rf_classifier = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
                rf_classifier.fit(X_train, y_train)

                # Evaluate the model
                y_pred = rf_classifier.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                st.write('### Model Evaluation')
                st.write(f'Accuracy: {accuracy:.2f}')


                # Additional plots
    # Plot 1: Confusion Matrix
                fig1, ax1 = plt.subplots()
                cm = confusion_matrix(y_test, y_pred)
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                st.pyplot(fig1)

    # Plot 2: ROC Curve
                fig2, ax2 = plt.subplots()
                fpr, tpr, thresholds = roc_curve(y_test, y_pred)
                plt.plot(fpr, tpr, color='blue', lw=2)
                plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                st.pyplot(fig2)

    # Plot 3: Precision-Recall Curve
                fig3, ax3 = plt.subplots()
                precision, recall, _ = precision_recall_curve(y_test, y_pred)
                plt.plot(recall, precision, color='green', lw=2)
                plt.xlabel('Recall')
                plt.ylabel('Precision')
                plt.title('Precision-Recall Curve')
                st.pyplot(fig3)

    # Plot 4: Probability Distributions of Predicted Classes
                fig4, ax4 = plt.subplots()
                sns.kdeplot(y_pred[y_test == 0], label='Class 0', shade=True)
                sns.kdeplot(y_pred[y_test == 1], label='Class 1', shade=True)
                plt.xlabel('Predicted Probability')
                plt.ylabel('Density')
                plt.title('Probability Distributions of Predicted Classes')
                plt.legend()
                st.pyplot(fig4)
  
    # Plot 5: Decision Boundaries (2D)
                if X_train.shape[1] == 2:  # Only plot if there are 2 features
                    fig5, ax5 = plt.subplots()
                    plot_decision_boundaries(rf_classifier, X_train, y_train, ax=ax5)
                    ax5.set_title('Decision Boundaries')
                    st.pyplot(fig5)

            elif model_name == 'Logistic Regression':
                
      
                st.write('### Logistic Regression Configuration')
                st.write(f'Regularization Parameter (C): {C}')

    # Train the model
                log_reg = LogisticRegression(C=C, random_state=42)
                log_reg.fit(X_train, y_train)

    # Evaluate the model
               
                y_pred = log_reg.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                st.write('### Model Evaluation')
                st.write(f'Accuracy: {accuracy}')

    # Plot feature coefficients for Logistic Regression
                coefficients = log_reg.coef_[0]
                plt.figure(figsize=(10, 6))
                sns.barplot(x=coefficients, y=X.columns)
                plt.xlabel('Coefficient Value')
                plt.ylabel('Features')
                plt.title('Feature Coefficients')
                st.pyplot()

    # Additional plots
    # Plot 1: Confusion Matrix
                fig1, ax1 = plt.subplots()
                cm = confusion_matrix(y_test, y_pred)
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                st.pyplot(fig1)

    # Plot 2: ROC Curve
                fig2, ax2 = plt.subplots()
                fpr, tpr, thresholds = roc_curve(y_test, y_pred)
                plt.plot(fpr, tpr, color='blue', lw=2)
                plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                st.pyplot(fig2)

    # Plot 3: Precision-Recall Curve
                fig3, ax3 = plt.subplots()
                precision, recall, _ = precision_recall_curve(y_test, y_pred)
                plt.plot(recall, precision, color='green', lw=2)
                plt.xlabel('Recall')
                plt.ylabel('Precision')
                plt.title('Precision-Recall Curve')
                st.pyplot(fig3)

    # Plot 4: Probability Distributions of Predicted Classes
                fig4, ax4 = plt.subplots()
                sns.kdeplot(y_pred[y_test == 0], label='Class 0', shade=True)
                sns.kdeplot(y_pred[y_test == 1], label='Class 1', shade=True)
                plt.xlabel('Predicted Probability')
                plt.ylabel('Density')
                plt.title('Probability Distributions of Predicted Classes')
                plt.legend()
                st.pyplot(fig4)

    # Plot 5: Scatter Plot of Actual vs Predicted
                fig5, ax5 = plt.subplots()
                ax5.scatter(y_test, y_pred, color='blue')
                ax5.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
                ax5.set_xlabel('Actual')
                ax5.set_ylabel('Predicted')
                ax5.set_title('Actual vs Predicted')
                st.pyplot(fig5)

            elif model_name == 'SVM':
                st.write('### SVM Configuration')
                st.write(f'Regularization Parameter (C): {C}')
                st.write(f'Kernel: {kernel}')

    # Train the model
                C = 1.0  # Default value for C
                svm_classifier = SVC(C=C, kernel=kernel, random_state=42)
                svm_classifier.fit(X_train, y_train)

    # Evaluate the model
         
                y_pred = svm_classifier.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                st.write('### Model Evaluation')
                st.write(f'Accuracy: {accuracy:.2f}')

    # Plot feature coefficients for SVM (absolute values)
                coefficients = np.abs(svm_classifier.coef_.flatten())  # Taking absolute values of coefficients
    # Ensure the lengths of coefficients and feature names match
                if len(coefficients) == len(X.columns):
                    fig1, ax1 = plt.subplots(figsize=(10, 6))
                    sns.barplot(x=coefficients, y=X.columns, ax=ax1)
                    ax1.set_xlabel('Absolute Coefficient Value')
                    ax1.set_ylabel('Features')
                    ax1.set_title('Feature Coefficients (Absolute Values)')
                    st.pyplot(fig1)
    # Additional plots
    # Plot 1: Confusion Matrix
                    fig2, ax2 = plt.subplots()
                    cm = confusion_matrix(y_test, y_pred)
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
                    plt.xlabel('Predicted')
                    plt.ylabel('Actual')
                    plt.title('Confusion Matrix')
                    st.pyplot(fig2)

    # Plot 2: ROC Curve
                    fig3, ax3 = plt.subplots()
                    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
                    plt.plot(fpr, tpr, color='blue', lw=2)
                    plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
                    plt.xlabel('False Positive Rate')
                    plt.ylabel('True Positive Rate')
                    plt.title('ROC Curve')
                    st.pyplot(fig3)

    # Plot 3: Precision-Recall Curve
                    fig4, ax4 = plt.subplots()
                    precision, recall, _ = precision_recall_curve(y_test, y_pred)
                    plt.plot(recall, precision, color='green', lw=2)
                    plt.xlabel('Recall')
                    plt.ylabel('Precision')
                    plt.title('Precision-Recall Curve')
                    st.pyplot(fig4)

    # Plot 4: Probability Distributions of Predicted Classes
                    fig5, ax5 = plt.subplots()
                    sns.kdeplot(y_pred[y_test == 0], label='Class 0', shade=True)
                    sns.kdeplot(y_pred[y_test == 1], label='Class 1', shade=True)
                    plt.xlabel('Predicted Probability')
                    plt.ylabel('Density')
                    plt.title('Probability Distributions of Predicted Classes')
                    plt.legend()
                    st.pyplot(fig5)

    # Plot 5: Scatter Plot of Actual vs Predicted
                    fig6, ax6 = plt.subplots()
                    ax6.scatter(y_test, y_pred, color='blue')
                    ax6.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
                    ax6.set_xlabel('Actual')
                    ax6.set_ylabel('Predicted')
                    ax6.set_title('Actual vs Predicted')
                    st.pyplot(fig6)

                
            elif model_name == 'K-Nearest Neighbors':
                st.write('### K-Nearest Neighbors Configuration')
                st.write(f'Number of Neighbors: {n_neighbors}')

    # Train the model
                knn_classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
                knn_classifier.fit(X_train, y_train)

    # Evaluate the model
               
                y_pred = knn_classifier.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                st.write('### Model Evaluation')
                st.write(f'Accuracy: {accuracy:.2f}')

    # Additional plots
    # Plot 1: Confusion Matrix
                fig1, ax1 = plt.subplots()
                cm = confusion_matrix(y_test, y_pred)
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                st.pyplot(fig1)

    # Plot 2: ROC Curve
                fig2, ax2 = plt.subplots()
                fpr, tpr, thresholds = roc_curve(y_test, y_pred)
                plt.plot(fpr, tpr, color='blue', lw=2)
                plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                st.pyplot(fig2)

    # Plot 3: Precision-Recall Curve
                fig3, ax3 = plt.subplots()
                precision, recall, _ = precision_recall_curve(y_test, y_pred)
                plt.plot(recall, precision, color='green', lw=2)
                plt.xlabel('Recall')
                plt.ylabel('Precision')
                plt.title('Precision-Recall Curve')
                st.pyplot(fig3)

    # Plot 4: Scatter Plot of Actual vs Predicted
                fig4, ax4 = plt.subplots()
                ax4.scatter(y_test, y_pred, color='blue')
                ax4.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
                ax4.set_xlabel('Actual')
                ax4.set_ylabel('Predicted')
                ax4.set_title('Actual vs Predicted')
                st.pyplot(fig4)

    # Plot 5: Decision Boundaries (2D)
                if X_train.shape[1] == 2:  # Only plot if there are 2 features
                    fig5, ax5 = plt.subplots()
                    plot_decision_boundaries(knn_classifier, X_train, y_train, ax=ax5)
                    ax5.set_title('Decision Boundaries')
                    st.pyplot(fig5)


            elif model_name == 'Decision Tree':
                st.write('### Decision Tree Configuration')
                st.write(f'Max Depth: {max_depth}')

    # Train the model
                dt_classifier = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
                dt_classifier.fit(X_train, y_train)

    # Evaluate the model
           
                y_pred = dt_classifier.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                st.write('### Model Evaluation')
                st.write(f'Accuracy: {accuracy:.2f}')

    # Plot feature importances
                feature_importances = dt_classifier.feature_importances_
                plt.figure(figsize=(10, 6))
                sns.barplot(x=feature_importances, y=X.columns)
                plt.xlabel('Feature Importance')
                plt.ylabel('Features')
                plt.title('Feature Importances')
                st.pyplot()

    # Additional plots
    # Plot 1: Confusion Matrix
                fig1, ax1 = plt.subplots()
                cm = confusion_matrix(y_test, y_pred)
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
                plt.xlabel('Predicted')
                plt.ylabel('Actual')
                plt.title('Confusion Matrix')
                st.pyplot(fig1)

    # Plot 2: ROC Curve
                fig2, ax2 = plt.subplots()
                fpr, tpr, thresholds = roc_curve(y_test, y_pred)
                plt.plot(fpr, tpr, color='blue', lw=2)
                plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('ROC Curve')
                st.pyplot(fig2)

    # Plot 3: Precision-Recall Curve
                fig3, ax3 = plt.subplots()
                precision, recall, _ = precision_recall_curve(y_test, y_pred)
                plt.plot(recall, precision, color='green', lw=2)
                plt.xlabel('Recall')
                plt.ylabel('Precision')
                plt.title('Precision-Recall Curve')
                st.pyplot(fig3)

    # Plot 4: Decision Tree Visualization
                fig4, ax4 = plt.subplots()
                plot_tree(dt_classifier, feature_names=X.columns, filled=True)
                plt.title('Decision Tree Visualization')
                st.pyplot(fig4)

    # Plot 5: Actual vs Predicted Scatter Plot
                fig5, ax5 = plt.subplots()
                ax5.scatter(y_test, y_pred, color='blue')
                ax5.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
                ax5.set_xlabel('Actual')
                ax5.set_ylabel('Predicted')
                ax5.set_title('Actual vs Predicted')
                st.pyplot(fig5)

       

            elif model_name == 'Linear Regression':
                st.write('### Linear Regression Configuration')

    # Train the model
                lin_reg = LinearRegression()
                lin_reg.fit(X_train, y_train)

    # Evaluate the model
            
                y_pred = lin_reg.predict(X_test)

                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Calculating RMSE
                r2 = r2_score(y_test, y_pred) 

                st.write('### Model Evaluation')
                st.write(f'Mean Squared Error: {mse:.2f}')
                st.write(f'Mean Absolute Error: {mae:.2f}')
                st.write(f'Root Mean Squared Error: {rmse:.2f}')
                st.write(f'R-squared: {r2:.2f}')  # Displaying R-squared score

    # Plotting predicted vs actual values
                fig, ax = plt.subplots()
                ax.scatter(y_test, y_pred, color='blue')
                ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
                ax.set_xlabel('Actual')
                ax.set_ylabel('Predicted')
                ax.set_title('Actual vs Predicted')
                st.pyplot(fig)

    # Additional plots
                fig1, ax1 = plt.subplots()
                ax1.hist(y_pred - y_test, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
                ax1.set_xlabel('Prediction Error')
                ax1.set_ylabel('Frequency')
                ax1.set_title('Error Histogram')
                st.pyplot(fig1)

                fig2, ax2 = plt.subplots()
                ax2.boxplot(y_pred - y_test)
                ax2.set_title('Boxplot of Prediction Error')

                st.pyplot(fig2)

                fig3, ax3 = plt.subplots()
                ax3.plot(y_test, label='Actual', color='blue')
                ax3.plot(y_pred, label='Predicted', color='red')
                ax3.set_xlabel('Index')
                ax3.set_ylabel('Value')
                ax3.set_title('Actual vs Predicted')
                ax3.legend()
                st.pyplot(fig3)

                fig4, ax4 = plt.subplots()
                ax4.bar(['MSE', 'MAE', 'RMSE', 'R-squared'], [mse, mae, rmse, r2], color=['blue', 'green', 'orange', 'red'])
                ax4.set_ylabel('Value')
                ax4.set_title('Model Evaluation Metrics')
                st.pyplot(fig4)

                fig5, ax5 = plt.subplots()
                ax5.plot(X_test[:100], y_test[:100], 'bo', label='Actual')  # Plotting a subset of data (first 100 points)
                ax5.plot(X_test[:100], y_pred[:100], 'r-', label='Predicted')
                ax5.set_xlabel('Feature')
                ax5.set_ylabel('Target')
                ax5.set_title('Actual vs Predicted')
                ax5.legend()
                st.pyplot(fig5)


if __name__ == "__main__":
    main()
