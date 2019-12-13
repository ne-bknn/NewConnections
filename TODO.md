# TODO

### Caching
- [ ] FileCache invalidation based on creation time
- [ ] Cache in Redis

### Algos
- [ ] Different clustering algos
- [x] Plotting feature
- [ ] **Efficient** community expansion algo

### Presentation
- [ ] Web app

### Misc
- [ ] OAuth2

### Known bugs
- [ ] Ego graphs generates with dublicate edges, Graph's \_\_init\_\_ needs to be fixed
- [ ] Unfortunately, edge betweenness works way to slow for large enough graphs. Need to add some graph size metric and use multilevel for large graphs.
- [ ] All tests that involve auth will fail if there is a 2fa present; temporary solution - authenticate manually. After that vk_api will save the token and allow these tests to pass.
- [ ] Some graphs will fail during dendrogram.as_clustering(). Added test. Needs to be fixed.
- [x] With multiple cache instances strange bugs occur, provided that we do not delete anything current a session. Needs to be investigated.
