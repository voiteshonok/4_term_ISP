import pytest

from .models import Tag
from datetime import datetime



# @pytest.fixture(scope="function")
# def model_user(db):
#     input_file = open("test_files/links_ZC9pVne.txt", 'r')
#     output_file = open("test_files/links_ZfM2DVv.txt", 'r')

#     post = Post.objects.create(
#         title="test",
#         slug="test",
#         body="test",
#         date_pub=datetime.now(),
#         input=input_file,
#         output=output_file
#     )
#     post.save()

#     yield post
    
#     input_file.close()
#     output_file.close()
#     post.delete()


def test_dometest():
    pass