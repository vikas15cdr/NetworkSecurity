Phishing Website Detection Pipeline
A Production-Grade End-to-End MLOps Project
This project implements a complete, production-grade machine learning pipeline to detect and classify phishing websites with high accuracy. It automates the entire workflow from data ingestion and preprocessing to model training, evaluation, and deployment preparation, leveraging a modern MLOps and cloud technology stack.

The final Random Forest model achieves an accuracy of 98.9% on the test dataset, demonstrating its effectiveness in enhancing online security.

🏛️ Cloud Architecture
The entire pipeline is designed for scalability and automation, leveraging key AWS services for a robust, serverless deployment. The model is trained on EC2 and deployed via AWS Lambda, making it cost-efficient and highly scalable.

The architecture includes:

Amazon S3: For scalable storage of the dataset and versioned model artifacts.

Amazon EC2: For providing on-demand compute resources for model training and hyperparameter tuning.

AWS Lambda & API Gateway: For deploying the final model as a serverless, real-time prediction API.

✨ Key Features
End-to-End Pipeline: Automates the entire machine learning workflow from raw data to a deployable model artifact.

Cloud-Native Deployment: Utilizes AWS (S3, EC2, Lambda) to build a scalable and production-ready solution.

High-Performance Model: Achieves 98.9% accuracy using a fine-tuned Random Forest classifier.

MLOps Integration: Uses MLflow and DagsHub for comprehensive experiment tracking, model versioning, and ensuring full project reproducibility.

🛠️ Tech Stack
Technology

Description

🐍 Python

Core programming language for the entire pipeline.

🤖 Scikit-learn

For building and evaluating the Random Forest model.

🐼 Pandas & NumPy

For efficient data manipulation, cleaning, and preprocessing.

☁️ AWS

Cloud platform for data storage (S3), training (EC2), and deployment (Lambda).

📊 MLflow & DagsHub

For MLOps, experiment tracking, and model lifecycle management.

📦 Git & GitHub

For version control and source code management.

⚙️ Project Workflow
The project is structured as a modular pipeline, with each component handling a specific task:

Data Ingestion: The phishing.csv dataset is loaded from a source (e.g., local or S3).

Data Transformation: The raw data undergoes preprocessing, including feature scaling, to prepare it for the machine learning models.

Model Training: Several classification models are trained on the preprocessed data. The Random Forest model was identified as the top performer through rigorous evaluation.

Experiment Tracking: During training, all experiments are logged to MLflow. This includes parameters, performance metrics (accuracy, F1-score), and the model artifact itself.

Model Deployment: The best-performing model is saved and packaged, ready to be deployed as a prediction service on AWS Lambda.

🚀 Getting Started
To run this project locally, follow these steps:

Prerequisites
Python 3.9+

Git

Installation & Setup
Clone the repository:

git clone [https://github.com/vikas15cdr/NetworkSecurity.git](https://github.com/vikas15cdr/NetworkSecurity.git)
cd NetworkSecurity

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:

pip install -r requirements.txt

Running the Pipeline
To execute the complete end-to-end training pipeline, run the main script:

python main.py

📈 Results
The best-performing model, Random Forest, achieved an outstanding accuracy of 98.9% on the test dataset, effectively distinguishing between legitimate and phishing websites. All experiment metrics and model versions are tracked and accessible via the DagsHub MLflow server.

💡 Future Scope
Integrate a CI/CD pipeline (e.g., GitHub Actions) to automate testing and deployment.

Experiment with deep learning models (e.g., Neural Networks) to potentially improve accuracy further.

Develop a simple front-end interface (e.g., using Streamlit or Flask) to interact with the deployed model API.

📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.
