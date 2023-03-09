sudo apt update
sudo apt -y install bzip2 git libxml2-dev
sudo apt -y install python3 pip

sudo pip3 install beautifulsoup4 gcloud glob2 virtualenv
sudo pip3 install google-api-core google-auth google-cloud-compute google-cloud-core google-cloud-storage

#Note: You can replace with your email address for the bash script
git config --global user.name 'Joe Brock'
git config --global user.email 'joebbrock3@gmail.com'

curl -u "Authorization: token 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" https://github.com/GoswamiSagarD/Team-Prophecy.git
git clone -b master https://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@github.com/GoswamiSagarD/Team-Prophecy.git
cd Team-Prophecy
python3 ./main.py
#THIS WORKS
#gcloud compute snapshots list --project tprophecy-378622 #<- For listing all snapshots under our project
gcloud compute images delete --quiet cec-snapshots
gcloud compute images create "cec-snapshot" \
  --source-disk "cec-instance-1" \
  --source-disk-zone "us-east4-c"
gcloud compute instance delete cec-instance-1 --quiet --zone=us-east4-c