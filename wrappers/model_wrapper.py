from transformers import GPT2LMHeadModel, GPT2Tokenizer

class ModelWrapper:
    """
    Base class for model wrappers.
    """
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        """
        Load the model and tokenizer. 
        Should be overridden by subclasses for specific models.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def generate_solution(self, test_case):
        """
        Use the loaded model to generate a solution for the test case.
        Should be overridden by subclasses for specific models.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


class GPT2Wrapper(ModelWrapper):
    """
    Wrapper for GPT-2 model from Hugging Face's transformers library.
    """
    def load_model(self):
        """
        Load the GPT-2 model and tokenizer based on the model_name.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)

    def generate_solution(self, test_case):
        """
        Use the GPT-2 model and tokenizer to generate a solution for the test case.
        """
        input_tensor = self.tokenizer.encode(test_case, return_tensors='pt')
        output = self.model.generate(input_tensor)
        solution = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return solution
