from filters.response_filter import ResponseFilter
import nltk


class PosTag:
    @staticmethod
    def tag(query):
        token = nltk.word_tokenize(query)
        tagged = nltk.pos_tag(token)

        return tagged


class EntityRecognition(ResponseFilter):
    def parse(self, current_repsonse, original_response, query):
        tagged = PosTag.tag(query)
        named_ent = nltk.ne_chunk(tagged, binary=True)

        ne_set = []
        for i in named_ent:
            if type(i) == nltk.tree.Tree:
                st = ""
                for j in range(len(i)):
                    st = st + " " + i[j][0]
                    ne_set.append(st.strip())
        if "Hello" in ne_set:
            ne_set.pop(0)
        if "Hi" in ne_set:
            ne_set.pop(0)
        if "Hey" in ne_set:
            ne_set.pop(0)

        if len(ne_set) > 0:
            check = query.split()

            if "they" in check:
                current_repsonse = (
                    "Please tell "
                    + ne_set[len(ne_set) - 1]
                    + ': "'
                    + current_repsonse
                    + '"'
                )
                self.lastname = True

            if "They" in check:
                current_repsonse = (
                    "Please tell "
                    + ne_set[len(ne_set) - 1]
                    + ': "'
                    + current_repsonse
                    + '"'
                )
                self.lastname = True
            if "their" in check:
                current_repsonse = (
                    "Please tell "
                    + ne_set[len(ne_set) - 1]
                    + ': "'
                    + current_repsonse
                    + '"'
                )
                self.lastname = True

            if "Their" in check:
                current_repsonse = (
                    "Please tell "
                    + ne_set[len(ne_set) - 1]
                    + ': "'
                    + current_repsonse
                    + '"'
                )
                self.lastname = True

            if "I'm" in check:
                current_repsonse = "Hello, " + ne_set[0] + ". " + current_repsonse
            else:
                if "They" in check:
                    current_repsonse = 'Tell them: "' + current_repsonse + '"'
                if "they" in check:
                    current_repsonse = 'Tell them: "' + current_repsonse + '"'

        return current_repsonse
