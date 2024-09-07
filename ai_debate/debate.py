class Debate:
    def __init__(self, model_a, model_b, judges, topic, fighter_a_view, fighter_b_view):
        self.fighter_a = model_a
        self.fighter_b = model_b
        self.judges = judges
        self.topic = topic
        self.fighter_a_view = fighter_a_view
        self.fighter_b_view = fighter_b_view
        self.context = (
            f"Debate on topic: {self.topic}\n"
            f"{self.fighter_a.model_name}'s viewpoint: {self.fighter_a_view}\n"
            f"{self.fighter_b.model_name}'s viewpoint: {self.fighter_b_view}\n"
        )

    def update_context(self, new_context):
        self.context += f"\n{new_context}"

    def fight_round(self, round_number):
        self.update_context(f"Round Number: {round_number}")
        
        if round_number % 2:
            model_a_response = self._generate_argument(self.fighter_a, "argument")
            model_b_response = self._generate_argument(self.fighter_b, "counter")
        else:
            model_b_response = self._generate_argument(self.fighter_b, "argument")
            model_a_response = self._generate_argument(self.fighter_a, "counter")

        return model_a_response, model_b_response

    def _generate_argument(self, fighter, arg_type):
        self.update_context(f"{'Argument' if arg_type == 'argument' else 'Counter Argument'} from {fighter.model_name}:")
        response = fighter.generate_result(self.context, arg_type, self.topic)
        self.update_context(response)
        return response

    def scoring(self, model_a_response, model_b_response):
        score_dict = {"model_a": [], "model_b": []}
        for judge in self.judges:
            score_dict["model_a"].append(judge.return_score(model_a_response, self.context))
            score_dict["model_b"].append(judge.return_score(model_b_response, self.context))

        score_a = sum(score_dict["model_a"]) / len(score_dict["model_a"])
        score_b = sum(score_dict["model_b"]) / len(score_dict["model_b"])

        return score_a, score_b