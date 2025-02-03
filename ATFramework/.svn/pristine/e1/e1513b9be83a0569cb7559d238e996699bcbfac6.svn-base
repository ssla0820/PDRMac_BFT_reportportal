from sentence_transformers import SentenceTransformer

class Compare():
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')

    def get_score(self, sentences):
        embeddings = self.model.encode(sentences)
        similarities = self.model.similarity(embeddings, embeddings)

        return [round(float(similarities[0][i]),4) for i in range(1, len(sentences))]
    
    
    def compare(self, sentence_list, criteria=0.99, criteria_list=None):
        '''
        sentences: list of sentences, ['test sentence', 'ground truth sentence 1', 'ground truth sentence 2', ...]
        criteria: float, similarity score threshold
        criteria_list: list of float, similarity score threshold for each sentence pair, leave it None if you want to use the same criteria for all sentence pairs

        socre_list = [compare result of test sentence with ground truth sentence 1, compare result of test sentence with ground truth sentence 2, ...]
        '''
        score_list = self.get_score(sentence_list)

        if criteria_list:
            if len(criteria_list) != len(score_list):
                raise ValueError('criteria_list length must be equal to the number of sentence pairs, please check your criteria_list')
            return [score >= criteria_list[i] for i, score in enumerate(score_list)], score_list, criteria_list
        else:
            return [score >= criteria for score in score_list], score_list, criteria


if __name__ == '__main__':
    sentences = ['I am a student', 'I am a teacher', 'I am a doctor']
    compare = Compare()

    # compare with criteria
    result = compare.compare(sentences, criteria=0.60)
    print(result)

    # compare with criteria_list
    result = compare.compare(sentences, criteria_list=[0.60, 0.50])
    print(result)