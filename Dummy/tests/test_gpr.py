import unittest


class TestGPR(unittest.TestCase):
    """ Tests
    """

    def setUp(self):
        """Set up
        Loads a model
        """
        self.protein = 'P15993'

    def test_gpr(self):
        """Tests gpr
        """
        from dummy.util.parsing import Boolean, build_tree, BooleanEvaluator
        expression = "( (Lrp AND NOT (leu_L_e_>0)) OR NOT(((GlnG AND GlnB AND GlnD) AND RpoN) AND ((glu_L_e_>0) OR \
                       (arg_L_e_>0) OR (asp_L_e_>0) OR (his_L_e_>0) OR (pro_L_e_>0) )))"
        t = build_tree(expression, Boolean)
        true_list = ['GlnG']
        # dict of variables values
        v = {'leu_L_e_': 1, 'glu_L_e_': 7, "arg_L_e_": 0.5,
             "asp_L_e_": 2, "his_L_e_": 0, "pro_L_e_": 0}
        evaluator = BooleanEvaluator(true_list, v)
        res = t.evaluate(evaluator.f_operand, evaluator.f_operator)
        print(res)
        self.assertEqual(res, True)
