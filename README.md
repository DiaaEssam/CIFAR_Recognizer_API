# CIFAR 100 Recognizier

## Description
The project is a Python-based application that implements an API for performing various tasks related to image classification using deep learning models. It provides functionalities for training and evaluating models such as AlexNet, ResNet-50, and transfer learning on the CIFAR-100 dataset.

## Project Structure
- `API.py`: The main file that defines the Flask API and contains the endpoints for the application.
- `alexnet_for_cifar_100.py`: File containing the implementation of the AlexNet model for CIFAR-100 dataset.
- `resnet_50_for_cifar_100.py`: File containing the implementation of the ResNet-50 model for CIFAR-100 dataset.
- `transfer_learning_on_cifar_100.py`: File containing the implementation of transfer learning on the CIFAR-100 dataset.
- `requirements.txt`: File specifying the dependencies required to run the application.
- `Dockerfile.txt`: File containing the Dockerfile instructions for containerizing the application.

## Getting Started
1. Clone the repository: `git clone <repository-url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python API.py`
4. Access the API endpoints at `http://localhost:5000`

## Usage
- Use the provided API endpoints to perform tasks such as model training, evaluation, and inference.
- Refer to the documentation in the respective Python files for more details on the implementation of each model and the available endpoints.

## Resources
- [CIFAR-100 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)
- [Flask](https://flask.palletsprojects.com/)
- [TensorFlow](https://www.tensorflow.org/)
- [Keras](https://keras.io/)

## License
This project is licensed under the [MIT License](LICENSE).
