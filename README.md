# CIFAR-100 Image Classification

- [Installation](#installation)
- [Usage](#usage)
- [Model](#model)
- [License](#license)

## Installation

To run the project, make sure you have the following dependencies installed:

- Python 3.6 or higher
- TensorFlow 2.0 or higher
- Keras 2.3 or higher
- NumPy
- Pandas
- Pillow
- scikit-learn
- Flask
- Flasgger

You can install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

## Usage

1. Run the Flask API:

```
python API.py
```

2. Access the Swagger UI by opening the following URL in your browser:

```
http://localhost:5000/apidocs/
```

3. Use the Swagger UI to interact with the API. You can predict the coarse label of a single image or a CSV file containing multiple images.

## Model

The model used in this project is based on the AlexNet architecture. It has been trained on the CIFAR-100 dataset, which consists of 50,000 training images and 10,000 test images. The model achieves an accuracy of XX% on the test set.

The 20 coarse labels predicted by the model are as follows:
- Aquatic mammals
- Fish
- Flowers
- Food containers
- Fruit and vegetables
- Household electrical devices
- Household furniture
- Insects
- Large carnivores
- Large man-made outdoor things
- Large natural outdoor scenes
- Large omnivores and herbivores
- Medium-sized mammals
- Non-insect invertebrates
- People
- Reptiles
- Small mammals
- Trees
- Vehicles 1
- Vehicles 2

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

Feel free to explore and modify the code to suit your needs. Contributions are welcome!
