python app.py --flag_do_torch_compile
python speed.py
import torch

# Assuming 'model' is your LivePortrait model and 'dummy_input' is a sample input tensor
torch.onnx.export(model, dummy_input, "liveportrait.onnx", opset_version=11)
import onnxruntime as ort
import numpy as np

# Load the ONNX model
session = ort.InferenceSession("liveportrait.onnx")

# Prepare input dictionary
inputs = {"input": dummy_input.numpy()}

# Run inference
outputs = session.run(None, inputs)
python inference.py --image_size 128
with torch.cuda.amp.autocast():
    output = model(input)
MLP = nn.Sequential(
    nn.Linear(256, 512),
    nn.ReLU(),
    nn.Linear(512, 128)
)
MLP = nn.Sequential(
    nn.Linear(128, 128),
    nn.ReLU(),
    nn.Linear(128, 64)
)
