from rest_framework import serializers
from rest_framework import validators
from api.models import ApiUser, Warehouse, Product, Transaction


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ApiUser
        fields = ('username', 'email', 'password', 'user_type')
        extra_kwargs = {
            'email': {'validators': [validators.UniqueValidator(ApiUser.objects.all())]}
        }

    def create(self, validated_data):
        user = ApiUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            password=validated_data['password']
        )
        return user


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ('quantity',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'product', 'transaction_type', 'quantity', 'created_at')
        read_only_fields = ('created_at', 'user')

    def validate(self, data):
        user = self.context['request'].user
        transaction_type = data.get('transaction_type')

        if user.user_type == 'provider' and transaction_type != 'supply':
            raise serializers.ValidationError("Поставщики могут только поставлять товар")
        if user.user_type == 'consumer' and transaction_type != 'consume':
            raise serializers.ValidationError("Потребители могут только забирать товар")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
