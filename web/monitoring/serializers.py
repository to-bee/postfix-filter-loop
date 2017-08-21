from rest_framework import serializers

from monitoring.models import Email
from rest_framework import serializers

from monitoring.models import Email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        # request = self.context['request']
        # labels = request.data.get('object')
        email = Email.objects.create(**validated_data)
        return email

    # def get_existing_email(self, email: Email):
    #     try:
    #         return Email.objects.get(id=email.id)
    #     except:
    #         return None
    #
    # def update(self, pk, validated_data):
    #     request = self.context['request']
    #
    #     print('Change label to: %s' % request.data.get('corrected_shortcut'))
    #     existing_prediction = Prediction.objects.get(id=request.data.get('id'))
    #
    #     corrected_shortcut = request.data.get('corrected_shortcut')
    #     if corrected_shortcut is None:
    #         raise serializers.ValidationError("Please select a label and approve again")
    #
    #     existing_prediction.corrected_shortcut = corrected_shortcut
    #     existing_prediction.validated = True
    #     current_img_dir = existing_prediction.image.path
    #     current_img_url = existing_prediction.image.url
    #     print('Current url,path: %s,%s' % (current_img_url, current_img_dir))
    #
    #     if os.path.isfile(current_img_dir):
    #         label = self.get_label_by_shortcut(existing_prediction)
    #         label_dir = os.path.join(env.get_data_dir(classifier_name=existing_prediction.classifier.name, type='train_new'), label)
    #         env.create_directory(label_dir)
    #
    #         (current_dir, name) = ntpath.split(current_img_dir)
    #         print(current_dir, name)
    #         if current_dir != label_dir:
    #             new_img_dir = os.path.join(label_dir, name)
    #             new_img_url = new_img_dir.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    #             print(new_img_url, new_img_dir)
    #
    #             os.rename(current_img_dir, new_img_dir)
    #             existing_prediction.image = new_img_dir.replace(settings.MEDIA_ROOT, '')
    #     else:
    #         print("Cannot move file because it doesn't exist: %s" % current_img_dir)
    #     existing_prediction.save()
    #     return existing_prediction
