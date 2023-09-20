from huggingface_hub import snapshot_download

if __name__ == "__main__":
    model_name = 'mattmdjaga/segformer_b2_clothes'
    local_dir = '../model'
    snapshot_download(repo_id=model_name, local_dir=local_dir)