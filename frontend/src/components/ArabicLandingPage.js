import React from 'react';
import { FaBrain, FaLanguage, FaDatabase, FaAtom, FaCubes } from 'react-icons/fa';
import styles from '../css/ArabicLandingPage.module.css';
import StockList from './StockList';
import CommodityList from './CommodityList';
import CryptocurrencyList from './CryptocurrencyList';
import '../css/StockList.css';
import '../css/CommodityList.css';
import '../css/CryptocurrencyList.css';
import '../css/UnifiedDetail.css';


const ArabicLandingPage = () => {
  return (
    <div className='detail-container'>
          <div className='detail-list'>
            <StockList />
            <CommodityList />
            <CryptocurrencyList />

          </div>
          <div>
              <div className={`${styles.container} ${styles.rtl}`}>
                      <section className={styles.section}>
                        <h1 className={styles.title}>مرحبًا بكم في بريدكس</h1>
                        <p className={styles.subtitle}>منصتكم المتقدمة للتنبؤ بالأصول المالية</p>
                      </section>

                      <section className={styles.section}>
                        <h2 className={styles.sectionTitle}>مهمتنا</h2>
                        <p className={styles.text}>
                          مهمتنا هي تمكين المستثمرين بالرؤى المبنية على البيانات، مما يتيح لهم اتخاذ قرارات مستنيرة في عالم الأسواق المالية سريعة التغير.
                        </p>
                      </section>

                      <section className={styles.section}>
                        <h2 className={styles.sectionTitle}>التكنولوجيا وراء تنبؤاتنا</h2>
                        <div className={styles.techGrid}>
                          <TechCard
                            icon={<FaBrain className={styles.icon} />}
                            title="الذكاء الاصطناعي والتعلم الآلي"
                            description="نماذج الذكاء الاصطناعي لدينا تتعلم باستمرار من كميات هائلة من البيانات السوقية."
                          />
                          <TechCard
                            icon={<FaLanguage className={styles.icon} />}
                            title="معالجة اللغة الطبيعية"
                            description="نحلل المقالات الإخبارية واتجاهات وسائل التواصل الاجتماعي والتقارير المالية في الوقت الفعلي."
                          />
                          <TechCard
                            icon={<FaDatabase className={styles.icon} />}
                            title="تحليلات البيانات الضخمة"
                            description="تعالج أنظمتنا تيرابايتات من البيانات المالية يوميًا."
                          />
                        </div>
                      </section>

                      <section className={styles.section}>
                        <h2 className={styles.sectionTitle}>ما يميزنا</h2>
                        <ul className={styles.list}>
                          <li>الدقة: تتفوق تنبؤاتنا باستمرار على طرق التحليل التقليدية.</li>
                          <li>الشمولية: نغطي مجموعة واسعة من الأصول، من الأسهم إلى العملات المشفرة.</li>
                          <li>تحديثات في الوقت الفعلي: يتم تحديث تنبؤاتنا في الوقت الفعلي مع تغير ظروف السوق.</li>
                        </ul>
                      </section>
                </div>
          </div>
    </div>

  );
};

const TechCard = ({ icon, title, description }) => {
  return (
    <div className={styles.techCard}>
      <div className={styles.iconWrapper}>{icon}</div>
      <h3 className={styles.cardTitle}>{title}</h3>
      <p>{description}</p>
    </div>
  );
};

export default ArabicLandingPage;


