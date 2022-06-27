# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine

class CareersPipeline:
    def process_item(self, item, spider):
        return item


if __name__ == '__main__':


    SQLALCHEMY_DATABASE_URI = 'postgresql://Shufan:1234@localhost/careers'
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    with engine.connect() as conn:

        sql = """
        INSERT INTO careers(Company, Job, Application, Category, Location)
        VALUES ('test','test','test','test', 'test')
        RETURNING Job
        """
        conn.execute(sql)


