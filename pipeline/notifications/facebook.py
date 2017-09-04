#coding: utf8
import facebook
from config import config

def main():
  cfg = {
    "page_id"      : config.get('facebook', 'page_id'),
    "access_token" : config.get('facebook', 'access_token')
    }

  api = get_api(cfg)
  msg = u"Here goes the message".encode('latin1')
  status = api.put_wall_post(msg)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph

if __name__ == "__main__":
  main()
