def predict_input(input_text):
    input_vector = preprocess_input(input_text)

    clf = load_model()

    pred = clf.predict(input_vector)

    return pred
