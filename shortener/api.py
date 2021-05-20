from flask import redirect, request, current_app, jsonify
from flask.views import MethodView
from hashids import Hashids

from .models import db, UrlsModel


hashids = Hashids(min_length=4, salt=current_app.config['SECRET_KEY'])


class UrlApi(MethodView):
    '''
    This class is api based on MethodView.
    '''
    def get(self, enc_url):
        '''
        1) Accept GET request on "host/api/" and returns all urls in db.
        2) Accept GET request on "host/<short_path>" and redirects
        to original url.
        '''
        if enc_url is None:
            data = UrlsModel.query.all()
            urls = [
                {
                    'id': url.id,
                    'short_url': url.short_url,
                    'original_url': url.original_url,
                    'redirects': url.redirects
                }
                for url in data
            ]
            return jsonify(urls=urls)
        else:
            url_id = hashids.decode(enc_url)[0]
            url = UrlsModel.query.filter_by(id=url_id).first()
            if url is not None:
                url.redirects += 1
                db.session.commit()
                return redirect(url.original_url)
            else:
                return jsonify(message=f'No url with id:{enc_url}')

    def post(self):
        '''
        Accepts POST reqest in json format on "host/api/":
        {
            "original_url": "http://yourlargeurl.com/"
        }

        returns json:
        {
            "short_url": "hostname/short_path"
        }
        '''
        if request.is_json:
            data = request.get_json()

            new_url = UrlsModel(original_url=data['original_url'])
            db.session.add(new_url)
            db.session.flush()
            short = hashids.encode(new_url.id)
            short_url = request.host + '/' + short
            new_url.short_url = short_url
            db.session.commit()

            return jsonify(short_url=short_url)
        else:
            return jsonify(error='wrong format!')

    def delete(self, enc_url):
        '''
        Accept DELETE request on "host/api/<short_path>".
        '''
        url_id = hashids.decode(enc_url)[0]
        url = UrlsModel.query.filter_by(id=url_id).first()
        if url is not None:
            db.session.delete(url)
            db.session.commit()
            return jsonify(message=f'url with short path:{enc_url} deleted!')
        else:
            return jsonify(message=f'No url with short path:{enc_url}')
