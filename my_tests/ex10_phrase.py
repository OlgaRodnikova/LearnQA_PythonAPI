class TestPhrase:
    def test_phrase_length(self):
        phrase = input("Введите фразу до 15 символов:")
        length_phrase = len(phrase)

        assert length_phrase < 15, "Длина фразы длиннее и равна 15 символам"
