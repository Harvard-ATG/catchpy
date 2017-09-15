import pytest

from model_mommy import mommy

from anno.anno_defaults import CATCH_CURRENT_SCHEMA_VERSION
from anno.anno_defaults import MEDIA_TYPES
from anno.models import Anno, Tag, Target

@pytest.mark.django_db
def test_relationships_ok():
    # create some tags
    tags = mommy.make(Tag, _quantity=3)

    # create annotations
    anno = mommy.make(Anno)
    anno.anno_tags = tags

    # create targets
    target = mommy.make(Target, anno=anno)
    assert(anno.anno_tags.count() == 3)
    assert(anno.target_set.count() == 1)


@pytest.mark.django_db
def test_target_ok():
    target = mommy.make(Target)
    assert(target.target_media in MEDIA_TYPES)
    assert(isinstance(target.anno, Anno))


@pytest.mark.django_db
def test_anno_ok():
    anno = mommy.make(Anno)
    assert(isinstance(anno, Anno))
    assert(anno.target_set.count() == 0)
    assert(anno.schema_version == CATCH_CURRENT_SCHEMA_VERSION)


@pytest.mark.django_db
def test_anno_object():
    anno = Anno(anno_id='123', raw='baba')
    tag1 = Tag(tag_name='tag1')
    tag1.save()
    anno.save()
    anno.anno_tags = [tag1]
    assert(anno.anno_tags.count() == 1)
    assert(Tag.objects.count() == 1)
    assert(tag1.anno_set.all()[0].anno_id == anno.anno_id)



