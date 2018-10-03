from django.test import TestCase

import real_estate.templatetags.real_estate_extras as extras


class Pymorhpy2TemplateTagTests(TestCase):
    def test_words_combined_with_hyphen_loct(self):
        """Test russian prepositional with hypen combined words
        It must change only last word"""
        hyphen_combined_word = 'Дизайн-квартал'

        # loct mean prepositional in pymorphy2
        # предложный (О ком? О чём? и т.п.) - хомяка несут в корзинке
        hyphen_combined_word_in_loct = 'Дизайн-квартале'

        # extras.morphy_by_case always returns low case
        hyphen_combined_word_in_loct = hyphen_combined_word_in_loct.lower()
        result = extras.morphy_by_case(hyphen_combined_word, 'loct')
        self.assertEqual(hyphen_combined_word_in_loct, result)

    def test_words_combined_with_hyphen_gent(self):
        """Test russian genitive with hypen combined words
        It must change only last word"""
        hyphen_combined_word = 'Дизайн-квартал'

        # gent mean genitive in pymorphy2
        # Родительный (Кого? Чего?) у нас нет хомяка
        hyphen_combined_word_in_gent = 'Дизайн-квартала'

        # extras.morphy_by_case always returns low case
        hyphen_combined_word_in_gent = hyphen_combined_word_in_gent.lower()
        result = extras.morphy_by_case(hyphen_combined_word, 'gent')
        self.assertEqual(hyphen_combined_word_in_gent, result)
