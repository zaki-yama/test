In-Context Cache Sample
=======================

NDB の In-Context Cache の機能を確認するためのサンプルコード



### In-Context Cache とは

- 1 リクエスト内で有効なキャッシュ
- 速度は In-Context Cache < Memcache < Datastore の順
	- In-Context Cache が microseconds に対し、Memcache は milliseconds とも

### In-Context Cache の効果を確認するためのサンプル：

```python
key = ndb.Key(MyModel, 'foo')  # この Key に対応するエンティティが存在するとして

obj1 = key.get()  # ここで datastore または memcache にアクセス (RPC が実行される)
obj2 = key.get()  # ここでは In-Context Cache が効いてるので RPC は実行されない
```

#### キャッシュのコントロール

```python
# context
ctx = ndb.get_context()

# Context Cache 無効
ctx.set_cache_policy(False)

# Memcache 無効
ctx.set_memcache_policy(False)

# Person クラスだけキャッシュしない
ctx.set_cache_policy(lambda key: key.kind() != 'Person')

# onetime
key.get(use_cache=False)

# clear all caches
ctx.clear_cache()
```



### References

(公式) https://cloud.google.com/appengine/docs/python/ndb/cache#incontext

http://ameblo.jp/cabeat-e/theme2-10061863878.html

http://blog.vier.jp/2013/02/google-app-engine-appengine-ja-night-23.html

https://docs.google.com/a/gigei.jp/presentation/d/1FDbkr0AoGxPOcEdaEjRb3ENxltxNxKTsdJW2PnmPU-8/edit#slide=id.g1ec03be_0_5

`set_cache_policy()` について
https://cloud.google.com/appengine/docs/python/ndb/contextclass#Context_set_cache_policy
