from celery import shared_task
from .models import Tenant, Transaction, ModelInfo
from django.conf import settings
import boto3, joblib, json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from io import BytesIO

@shared_task
def train_model_task(tenant_id, n_clusters=3):
    t = Tenant.objects.get(pk=tenant_id)
    trans = Transaction.objects.filter(tenant=t)
    X = [[tx.data['amount'], tx.data['hour'], tx.data['device_score']] for tx in trans]
    X_scaled = StandardScaler().fit_transform(X)
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)

    buf = BytesIO()
    joblib.dump(model, buf)
    buf.seek(0)
    s3 = boto3.client('s3')
    key = f"{tenant_id}/kmeans-{t.pk}-{int(t.trained_at.timestamp())}.joblib"
    s3.upload_fileobj(buf, settings.AWS_S3_BUCKET_NAME, key)

    mi = ModelInfo.objects.create(
        tenant=t,
        model_type='KMeans',
        metrics={'silhouette': score},
        s3_path=key,
        is_active=False
    )
    return {'model_id': mi.id, 'silhouette': score}
