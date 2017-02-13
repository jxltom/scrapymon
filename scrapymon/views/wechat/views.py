from scrapymon import wechat


@wechat.filter('_')
def wechat_test():
    return 'success'
