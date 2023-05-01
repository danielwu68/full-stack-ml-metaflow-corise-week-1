from metaflow import FlowSpec, step, card, current
from metaflow.cards import Table, Markdown, Artifact


class BSTFlow(FlowSpec):
    """
    train a boosted tree
    """

    @card
    @step
    def start(self):
        """
        Load the data & train model
        """
        import xgboost as xgb

        dtrain = xgb.DMatrix("data/agaricus.txt.train")
        param = {
            "max_depth": 2,
            "eta": 1,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
        }
        num_round = 2
        bst = xgb.train(param, dtrain, num_round)
        bst.save_model("model.json")
        self.next(self.predict)

    @step
    def predict(self):
        """
        make predictions
        """
        import xgboost as xgb

        dtest = xgb.DMatrix("data/agaricus.txt.test")
        # make prediction
        bst = xgb.Booster()
        bst.load_model("model.json")
        preds = bst.predict(dtest)
        self.preds = preds
        self.next(self.end)

    @card
    @step
    def end(self):
        """
        End of flow!
        """
        current.card.append(Markdown('## Result'))
        print("Results:", self.preds)
        print("BSTFlow is all done.")


if __name__ == "__main__":
    BSTFlow()
