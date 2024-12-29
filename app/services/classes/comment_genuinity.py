# external modules import
import re
from collections import Counter

# internal module imports
from app.services.classes.comment import Comment
from app.database.post_db import read_post
from app.services.comment_genuinity_helper.tlds import tlds
from app.services.comment_genuinity_helper.likely_spam_phrases import spam_phrases
from app.services.comment_genuinity_helper.comment_exclusions import relevancy_exclusions, keyword_stuffing_exclusions

# define a class which takes in the comment and analyses it by passing it to various methods within the class and ultimately decides the genuinity score in the __init__ method.
class CommentGenuinity(Comment):
    GENUINITY_SCORE = 0
    GENUINITY_SCORE_CUTOFF = 3
    MIN_RELEVANCY_SCORE = 1
    MAX_WORD_OCCURRENCE = 2

    def __init__(self, comment: str, post_id: int):
        self.comment = comment
        self.post_id = post_id

        checks = [self.relevancy_check, self.link_check, self.phrase_check, self.uppercase_check, self.stuffing_check]
        for check in checks:
            if check():
                self.GENUINITY_SCORE += 1

    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self, comment: str):
        self._comment = comment

    @property
    def post_id(self):
        return self._post_id
    
    @post_id.setter
    def post_id(self, post_id: int):
        self._post_id = post_id

    # fetch the post from the database and return as a dictionary
    def post(self) -> list[str]:
        post = read_post(self.post_id)
        post = re.sub(r"[\.,\?\:\+!'\"]", "", post.post_content.lower())
        return post.split()
    
    # convert the comment to a list so that it can be reused across methods
    def comment_to_list(self) -> list[str]:
        comment = re.sub(r"[\.,\?\:\+!'\"]", "", self.comment.lower())
        return comment.split()

    # checks how relevant the comment is to the post
    def relevancy_check(self) -> bool:

        """
        Score a comment on its relevancy to the post by checking if it contains words from the post that match these criteria:

        1. are at least 5 letters long (skipping generic words like "are", "and", "for", etc)
        2. are included in the exclusions list in the comment_exclusions.py file (generic words)

        Next, a relevancy score count is introduced and incremented each time a word in the comment matches any word in the post.
        Returns:
            bool:   True if the count is at least 2, indicating the check passed
                    False if the count is less than 2, indicating the check failed
        """
        self.relevant_words = set()
        post = self.post()
        for word in post:
            if len(word) > 4 and word not in relevancy_exclusions:
                self.relevant_words.add(word)
        
        relevancy_count = 0
        comment = self.comment_to_list()
        for word in comment:
            if word in self.relevant_words:
                relevancy_count += 1
        return relevancy_count > self.MIN_RELEVANCY_SCORE
    
    # checks if the comment contains a link
    def link_check(self) -> bool:

        """
        Looks for a TLD in the comment (using tlds, an external file) which will indicate a link. Uses self.comment instead of comment_to_list() so as to preserve punctuation - needed to match TLDs.
        Returns:
            bool:   True if the comment contains no link
                    False if the comment contains a link
        """
        comment = self.comment.split()
        for word in comment:
            for tld in tlds:
                if tld.lower() in word.lower():
                    return False
        return True

    # check if the comment contains a spam phrase from a set in an external file "likely spam phrases"
    def phrase_check(self) -> bool:

        """
        Since we need the entire comment as-is as opposed to an iterable list, we won't be using the comment_to_list() function. Rather, we use self.comment.
        Returns:
            bool:   True if the comment does not contain any suspicious phrases
                    False if the comment contains a suspicious phrase
        """
        for phrase in spam_phrases:
            if phrase.lower() in self.comment.lower():
                return False
        return True

    # check if the comment is all in uppercase
    def uppercase_check(self) -> bool:
        
        """
        Uses a one-liner to check that the comment is not in uppercase.
        Returns:
            bool:   True if the comment is not in uppercase
                    False if the comment is in uppercase, failing the check
        """

        return not self.comment.isupper()

    # check if the comment is keyword-stuffed (has repeated words)
    def stuffing_check(self) -> bool:
        
        """
        Uses Counter from collections to count how often each word occurs in the comment, ensures that the word is not in the relevant words from the post keyword_stuffing_exclusions set (defined in an external file), and checks the number of times the word occurs against a predetermined number.
        Returns:
            bool:   True if no word occurs in the comment at least 3 times
                    False if any word occurs in the comment at least 3 times
        """

        comment = self.comment_to_list()
        occurrences = Counter(comment) # Counter({"word": 5, "now": 3})
        for word in comment:
            for occurrence in occurrences:
                if word == occurrence and word not in self.relevant_words and word not in keyword_stuffing_exclusions and occurrences[occurrence] > self.MAX_WORD_OCCURRENCE:
                    return False
        return True